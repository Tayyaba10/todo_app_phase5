from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from typing import Optional
from sqlmodel import Session
from slowapi import Limiter
from slowapi.util import get_remote_address
from ...core.database import get_session
from ...services.gemini_agent_service import GeminiAgentService
from ...api.deps import get_current_user
from ...api.schemas.conversation import ChatRequest, ChatResponse
import os
import logging
from fastapi import Request


# Set up logging
logger = logging.getLogger(__name__)

# Initialize rate limiter for this router
limiter = Limiter(key_func=get_remote_address)

# Initialize router
router = APIRouter()


@router.post("/chat/{user_id}", response_model=ChatResponse)
@limiter.limit("10/minute")  # Limit to 10 requests per minute per IP
def chat(
    user_id: UUID,
    request: Request,
    chat_request: ChatRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """
    Process a chat message through the AI agent.
    """
    logger.info(f"Received chat request for user {user_id}, conversation {chat_request.conversation_id}")

    # Verify that the user_id in the path matches the authenticated user
    if str(current_user["user_id"]) != str(user_id):
        logger.warning(f"Access denied: user {current_user['user_id']} tried to access {user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Cannot access another user's chat"
        )

    # Get Gemini API key from environment
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        logger.error("Gemini API key not configured")
        raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Gemini API key not configured"
    )

    # Initialize agent service
    agent_service = GeminiAgentService(db_session=db, gemini_api_key=gemini_api_key)

    try:
        # Process the message through the agent
        result = agent_service.process_user_message(
            user_id=user_id,
            message_content=chat_request.message,
            conversation_id=chat_request.conversation_id
        )
        logger.info(f"Successfully processed message for user {user_id}, conversation {result['conversation_id']}")
        return ChatResponse(**result)
    except Exception as e:
        logger.error(f"Error processing message for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing message: {str(e)}"
        )


# Health check endpoint
@router.get("/health")
def health_check():
    logger.info("Health check endpoint called")
    return {"status": "healthy", "service": "chat-api"}