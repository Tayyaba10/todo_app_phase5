from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
from .task_tag import TaskTag  # Import the association table

if TYPE_CHECKING:
    from .task import Task

class TagBase(SQLModel):
    name: str = Field(unique=True, index=True, max_length=100, min_length=1)


class Tag(TagBase, table=True):
    __tablename__ = "tags"

    id: int = Field(default=None, primary_key=True)

    # Relationship with tasks through the association table
    tasks: list["Task"] = Relationship(
        back_populates="tags",
        link_model=TaskTag
    )


class TagCreate(TagBase):
    pass


class TagRead(TagBase):
    id: int

    class Config:
        from_attributes = True