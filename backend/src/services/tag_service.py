from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
from ..models.tag import Tag, TagCreate, TagRead
from ..models.task import Task
from ..models.task_tag import TaskTag
from ..core.exceptions import TagNotFoundException
from src.models import task_tag


class TagService:
    """
    Service class to handle tag-related business logic.
    """

    @staticmethod
    def create_tag(session: Session, tag_create: TagCreate) -> TagRead:
        """
        Create a new tag or return existing one if it already exists.
        """
        # Check if tag already exists
        existing_tag = session.exec(select(Tag).where(Tag.name == tag_create.name)).first()
        if existing_tag:
            return TagRead.model_validate(existing_tag) if hasattr(TagRead, 'model_validate') else TagRead(
                id=existing_tag.id,
                name=existing_tag.name
            )

        # Create a new tag
        db_tag = Tag(name=tag_create.name)
        session.add(db_tag)
        session.commit()
        session.refresh(db_tag)

        return TagRead.model_validate(db_tag) if hasattr(TagRead, 'model_validate') else TagRead(
            id=db_tag.id,
            name=db_tag.name
        )

    @staticmethod
    def get_tag_by_id(session: Session, tag_id: int) -> Optional[TagRead]:
        """
        Get a specific tag by ID.
        """
        statement = select(Tag).where(Tag.id == tag_id)
        tag = session.exec(statement).first()

        if not tag:
            raise TagNotFoundException(tag_id)

        return TagRead.model_validate(tag) if hasattr(TagRead, 'model_validate') else TagRead(
            id=tag.id,
            name=tag.name
        )

    @staticmethod
    def get_all_tags(session: Session) -> List[TagRead]:
        """
        Get all tags.
        """
        statement = select(Tag)
        tags = session.exec(statement).all()

        result = []
        for tag in tags:
            result.append(
                TagRead.model_validate(tag) if hasattr(TagRead, 'model_validate') else TagRead(
                    id=tag.id,
                    name=tag.name
                )
            )

        return result

    @staticmethod
    def assign_tag_to_task(session: Session, task_id: UUID, tag_name: str) -> bool:
        """
        Assign a tag to a task. Creates the tag if it doesn't exist.
        """
        # Get or create the tag
        tag_create = TagCreate(name=tag_name)
        tag = TagService.create_tag(session, tag_create)

        # Check if the association already exists
        existing_assoc = session.exec(
            select(TaskTag).where(
                TaskTag.task_id == task_id,
                TaskTag.tag_id == tag.id
            )
        ).first()

        if existing_assoc:
            # Association already exists, nothing to do
            return True

        # Create the association
        session.execute(
            TaskTag.insert().values(
                task_id=task_id,
                tag_id=tag.id
            )
        )
        session.commit()
        return True

    @staticmethod
    def remove_tag_from_task(session: Session, task_id: UUID, tag_id: int) -> bool:
        """
        Remove a tag from a task.
        """
        session.execute(
            TaskTag.delete().where(
                TaskTag.task_id == task_id,
                TaskTag.tag_id == tag_id
            )
        )
        session.commit()
        return True

    @staticmethod
    def get_tasks_by_tag(session: Session, tag_id: int) -> List[dict]:
        """
        Get all tasks associated with a specific tag.
        """
        statement = select(Task).join(TaskTag).where(
            TaskTag.tag_id == tag_id
        )
        tasks = session.exec(statement).all()

        result = []
        for task in tasks:
            # Get all tags for this task
            task_tags_statement = select(Tag).join(TaskTag).where(
                TaskTag.task_id == task.id
            )
            tags = session.exec(task_tags_statement).all()

            result.append({
                "id": str(task.id),
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "user_id": str(task.user_id),
                "created_at": task.created_at,
                "updated_at": task.updated_at,
                "priority": task.priority,
                "due_date": task.due_date,
                "reminder_time": task.reminder_time,
                "recurrence_type": task.recurrence_type,
                "recurrence_metadata": task.recurrence_metadata,
                "tags": [{"id": tag.id, "name": tag.name} for tag in tags]
            })

        return result