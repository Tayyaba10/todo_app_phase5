from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
from uuid import UUID
from sqlalchemy import Table, Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID

if TYPE_CHECKING:
    from .task import Task
    from .tag import Tag

# Association table for the many-to-many relationship between Task and Tag
# TaskTag = Table(
#     "task_tags",
#     SQLModel.metadata, 
#     Column("task_id", Integer, ForeignKey("tasks.id"),primary_key=True),
#     Column("tag_id", Integer, ForeignKey("tags.id"),primary_key=True)
# )

class TaskTag(SQLModel, table=True):
    __tablename__ = "task_tags"
    task_id: UUID = Field(foreign_key="tasks.id", primary_key=True)
    tag_id: int = Field(foreign_key="tags.id", primary_key=True)