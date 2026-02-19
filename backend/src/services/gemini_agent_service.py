import google.generativeai as genai
from typing import Dict, Any, Optional, List
from uuid import UUID
from datetime import datetime
from ..models.conversation import Conversation
from ..models.message import Message, SenderType
from ..services.task_service import TaskService
from ..services.conversation_service import ConversationService
from ..services.message_service import MessageService
from sqlmodel import Session
import json
import logging
import re

logger = logging.getLogger(__name__)

class GeminiAgentService:
    def __init__(self, db_session: Session, gemini_api_key: str):
        self.db_session = db_session
        

        # Require the API key to be provided
        if not gemini_api_key:
            raise ValueError("Gemini API key is required")

        self.gemini_api_key = gemini_api_key
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

        # TaskService uses static methods, so we don't instantiate it
        # We'll call its methods directly and pass the session as needed
        self.conversation_service = ConversationService(db_session)
        self.message_service = MessageService(db_session)

    def process_user_message(
        self,
        user_id: UUID,
        message_content: str,
        conversation_id: Optional[UUID] = None
    ) -> Dict[str, Any]:
        """
        Process a user message through the Gemini AI agent and return the response.
        """
        # Get or create conversation
        if conversation_id:
            conversation = self.conversation_service.get_conversation_by_id_with_messages(conversation_id)
        else:
            # Create new conversation
            from ..models.conversation import ConversationCreate
            conversation_data = ConversationCreate(user_id=user_id, title=message_content[:50])
            conversation = self.conversation_service.create_conversation(conversation_data)

        if not conversation:
            raise ValueError("Could not create or retrieve conversation")

        # Save user message using conversation service
        self.conversation_service.save_user_message(
            conversation_id=conversation.id,
            content=message_content
        )

        # Retrieve conversation history for context
        conversation_history = self.conversation_service.get_conversation_history(conversation.id)

        # Prepare the system prompt with available tools
        system_prompt = (
            "You are a helpful AI assistant that manages todos for users. "
            "Use the available functions to create, list, update, and delete tasks. "
            "Always respond in a friendly and helpful manner.\n\n"
            "Available functions:\n"
            "1. create_todo(title, description) - Create a new todo item\n"
            "2. list_todos() - List all todo items for the user\n"
            "3. update_todo(todo_id, title, description, completed) - Update a todo item\n"
            "4. delete_todo(todo_id) - Delete a todo item\n"
            "5. request_clarification(question) - Request clarification from the user\n\n"
            "When you need to call a function, respond with JSON in this exact format:\n"
            '{"function_call": {"name": "function_name", "arguments": {"arg1": "value1", "arg2": "value2"}}}\n\n'
            "If you don't need to call a function, respond normally."
        )

        # Build the conversation in a way that mimics chat history
        chat_history = []

        # Add system prompt as the first message
        chat_history.append({
            "role": "user",
            "parts": [{"text": system_prompt}]
        })
        chat_history.append({
            "role": "model",
            "parts": [{"text": "Okay, I understand. I'm ready to help you manage your todos using the available functions. How can I assist you today?"}]
        })

        # Add conversation history to chat history
        for msg in conversation_history:
            role = "user" if msg.sender_type == SenderType.user else "model"
            chat_history.append({
                "role": role,
                "parts": [{"text": msg.content}]
            })

        try:
            # Create a chat session with the history
            chat = self.model.start_chat(history=chat_history)

            # Send the message to the model
            response = chat.send_message(message_content)

            response_text = response.text if response.text else "I'm sorry, I couldn't generate a response. Please try again."

            # Check if the response contains a function call
            function_call_detected = self._extract_function_call(response_text)

            if function_call_detected:
                function_name = function_call_detected['name']
                function_args = function_call_detected['arguments']

                # Execute the tool with retry logic
                result = self._execute_tool_with_retry(function_name, function_args, user_id)

                # Format the tool result
                tool_result = self._handle_tool_execution_errors(result)

                # Follow up with the tool result to get final response
                follow_up_prompt = f"The function '{function_name}' was executed with the following result: {tool_result}. Based on this, provide a natural response to the user's original request."

                try:
                    final_response = chat.send_message(follow_up_prompt)
                    agent_reply = final_response.text if final_response.text else f"I've processed your request. The result was: {tool_result}"
                except Exception as e:
                    # Handle error in final response generation
                    agent_reply = f"I processed your request ({function_name}) successfully but encountered an error generating the final response: {str(e)}. The action was likely completed."
            else:
                # No function call needed, just return the model's response
                agent_reply = response.text

        except Exception as e:
            logger.error(f"Error calling Gemini API: {str(e)}")
            agent_reply = f"I encountered an error processing your request: {str(e)}. Please try again later."

        # Save agent response using conversation service
        self.conversation_service.save_agent_message(
            conversation_id=conversation.id,
            content=agent_reply
        )

        return {
            "response": agent_reply,
            "conversation_id": conversation.id,
            "tool_calls": []  # Gemini doesn't return structured tool calls like OpenAI
        }

    def _extract_function_call(self, response_text: str) -> Optional[Dict[str, Any]]:
        """
        Extract function call from Gemini response if it contains one.
        """
        try:
            # First, try to find JSON objects in the response
            # Look for patterns like {"function_call": {"name": "...", "arguments": {...}}}
            json_match = re.search(r'\{[^{}]*(?:\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}[^{}]*)*\}', response_text)

            if json_match:
                json_str = json_match.group(0)
                # Clean up potential escape characters
                json_str = json_str.strip()

                try:
                    parsed = json.loads(json_str)

                    if 'function_call' in parsed:
                        function_call = parsed['function_call']
                        if 'name' in function_call and 'arguments' in function_call:
                            return {
                                'name': function_call['name'],
                                'arguments': function_call['arguments']
                            }
                    elif 'name' in parsed and 'arguments' in parsed:
                        # Direct function call format
                        return {
                            'name': parsed['name'],
                            'arguments': parsed['arguments']
                        }

                except json.JSONDecodeError:
                    # If the initial parsing fails, try to fix common JSON issues
                    try:
                        # Attempt to fix common JSON issues
                        fixed_json = json_str.replace("\\'", "'").replace('\\"', '"')
                        parsed = json.loads(fixed_json)

                        if 'function_call' in parsed:
                            function_call = parsed['function_call']
                            if 'name' in function_call and 'arguments' in function_call:
                                return {
                                    'name': function_call['name'],
                                    'arguments': function_call['arguments']
                                }
                        elif 'name' in parsed and 'arguments' in parsed:
                            return {
                                'name': parsed['name'],
                                'arguments': parsed['arguments']
                            }
                    except json.JSONDecodeError:
                        pass
        except Exception:
            pass

        # If JSON parsing didn't work, try regex patterns for common formats
        function_patterns = [
            r'"function_call"\s*:\s*\{\s*"name"\s*:\s*"([^"]+)"\s*,\s*"arguments"\s*:\s*({.*?})\s*\}',
            r'"name"\s*:\s*"([^"]+)"\s*,\s*"arguments"\s*:\s*({.*?})',
            r'\{\s*"name"\s*:\s*"([^"]+)"\s*,\s*"arguments"\s*:\s*({.*?})\s*\}'
        ]

        for pattern in function_patterns:
            match = re.search(pattern, response_text)
            if match:
                func_name = match.group(1)
                args_str = match.group(2)
                try:
                    args = json.loads(args_str)
                    return {
                        'name': func_name,
                        'arguments': args
                    }
                except json.JSONDecodeError:
                    # If JSON parsing fails, try to extract basic key-value pairs
                    # This is a fallback for malformed JSON
                    arg_pattern = r'"(\w+)"\s*:\s*"([^"]*)"'
                    arg_matches = re.findall(arg_pattern, args_str)
                    args = {key: value for key, value in arg_matches}
                    if args:
                        return {
                            'name': func_name,
                            'arguments': args
                        }

        return None

    def _execute_tool(self, function_name: str, function_args: Dict[str, Any], user_id: UUID) -> Any:
        """
        Execute the specified tool with the given arguments.
        """
        from .task_service import TaskService
        from ..api.schemas.task import TaskCreateRequest, TaskUpdateRequest

        try:
            if function_name == "create_todo":
                # Create a TaskCreateRequest object with the provided args
                task_create = TaskCreateRequest(**function_args)
                return TaskService.create_task(self.db_session, task_create, user_id)
            elif function_name == "list_todos":
                return TaskService.get_tasks_by_user(self.db_session, user_id)
            elif function_name == "update_todo":
                if "todo_id" in function_args:
                    todo_id = function_args.pop("todo_id")
                    # Create a TaskUpdateRequest object with the remaining args
                    task_update = TaskUpdateRequest(**function_args)
                    return TaskService.update_task(self.db_session, todo_id, task_update, user_id)
                else:
                    return {"error": "todo_id is required for update_todo"}
            elif function_name == "delete_todo":
                todo_id = function_args.get("todo_id")
                if not todo_id:
                    return {"error": "todo_id is required for delete_todo"}
                return TaskService.delete_task(self.db_session, todo_id, user_id)
            elif function_name == "request_clarification":
                # Return the question to ask the user for clarification
                return {"clarification_needed": function_args.get("question", "I need more information to help you")}
            else:
                return {"error": f"Unknown function: {function_name}"}
        except Exception as e:
            return {"error": f"Error executing {function_name}: {str(e)}"}

    def _handle_tool_execution_errors(self, tool_call_result: Any) -> str:
        """
        Handle errors from tool execution and format appropriate responses.
        """
        if isinstance(tool_call_result, dict) and "error" in tool_call_result:
            return tool_call_result["error"]
        return str(tool_call_result)

    def _execute_tool_with_retry(self, function_name: str, function_args: Dict[str, Any], user_id: UUID, max_retries: int = 3) -> Any:
        """
        Execute a tool with retry logic for failed calls.
        """
        last_exception = None

        for attempt in range(max_retries):
            try:
                result = self._execute_tool(function_name, function_args, user_id)
                # If successful, return the result
                if not (isinstance(result, dict) and "error" in result):
                    return result
                # If it's a known error that shouldn't be retried, return it
                if "clarification_needed" in result:
                    return result
            except Exception as e:
                last_exception = e
                # Wait briefly before retrying (could implement exponential backoff)
                import time
                time.sleep(0.5)

        # If all retries failed, return the error
        if last_exception:
            return {"error": f"Error executing {function_name} after {max_retries} attempts: {str(last_exception)}"}
        else:
            return {"error": f"Error executing {function_name} after {max_retries} attempts"}