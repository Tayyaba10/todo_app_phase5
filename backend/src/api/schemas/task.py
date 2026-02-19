from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from uuid import UUID


# Request schemas
class TaskCreateRequest(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: str = "Medium"  # Low, Medium, High, Critical
    due_date: Optional[datetime] = None
    reminder_time: Optional[datetime] = None
    recurrence_type: Optional[str] = None  # daily, weekly, monthly
    recurrence_metadata: Optional[str] = None


class TaskUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None  # Low, Medium, High, Critical
    due_date: Optional[datetime] = None
    reminder_time: Optional[datetime] = None
    recurrence_type: Optional[str] = None  # daily, weekly, monthly
    recurrence_metadata: Optional[str] = None


class TaskToggleCompleteRequest(BaseModel):
    completed: bool


# Response schemas
class TagResponse(BaseModel):
    id: int
    name: str


class TaskResponse(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    completed: bool
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    priority: str = "Medium"  # Low, Medium, High, Critical
    due_date: Optional[datetime] = None
    reminder_time: Optional[datetime] = None
    recurrence_type: Optional[str] = None  # daily, weekly, monthly
    recurrence_metadata: Optional[str] = None
    tags: List[TagResponse] = []


class TaskListResponse(BaseModel):
    tasks: List[TaskResponse]


class MessageResponse(BaseModel):
    message: str