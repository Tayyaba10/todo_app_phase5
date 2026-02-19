from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, Optional, List
from datetime import datetime, date
from uuid import UUID, uuid4
#from .user import User

if TYPE_CHECKING:
    from .user import User   # ✅ only for typing
    from .tag import Tag

# Import the association table
from .task_tag import TaskTag

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)


class Task(TaskBase, table=True):
    __tablename__ = "tasks"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})

    # Advanced features fields
    priority: str = Field(default="Medium", max_length=20)  # Low, Medium, High, Critical
    due_date: Optional[datetime] = Field(default=None)  # Optional due date
    reminder_time: Optional[datetime] = Field(default=None)  # Optional reminder time
    recurrence_type: Optional[str] = Field(default=None, max_length=20)  # daily, weekly, monthly
    recurrence_metadata: Optional[str] = Field(default=None, max_length=500)  # Additional recurrence data

    # Relationship to user
    user: Optional["User"] = Relationship(back_populates="tasks")

    # Relationship to tags
    tags: List["Tag"] = Relationship(
        back_populates="tasks",
        link_model=TaskTag
    )


class TaskCreate(TaskBase):
    priority: Optional[str] = "Medium"  # Low, Medium, High, Critical
    due_date: Optional[datetime] = None
    reminder_time: Optional[datetime] = None
    recurrence_type: Optional[str] = None  # daily, weekly, monthly
    recurrence_metadata: Optional[str] = None


class TaskRead(TaskBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    priority: str
    due_date: Optional[datetime]
    reminder_time: Optional[datetime]
    recurrence_type: Optional[str]
    recurrence_metadata: Optional[str]


class TaskUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = None
    priority: Optional[str] = Field(default=None, max_length=20)  # Low, Medium, High, Critical
    due_date: Optional[datetime] = None
    reminder_time: Optional[datetime] = None
    recurrence_type: Optional[str] = Field(default=None, max_length=20)  # daily, weekly, monthly
    recurrence_metadata: Optional[str] = None


class TaskToggleComplete(SQLModel):
    completed: bool