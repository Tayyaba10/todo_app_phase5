from sqlmodel import SQLModel
from .task_tag import TaskTag
from .user import User
from .task import Task
from .tag import Tag
from .message import Message
from .conversation import Conversation

# Base SQLModel class that all models will inherit from
Base = SQLModel

# Import all models to ensure they are registered with SQLModel
__all__ = ["Base","TaskTag", "User", "Task", "Tag", "Message", "Conversation"]