from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
import datetime
from ..models.task import Task, TaskCreate, TaskUpdate, TaskToggleComplete
from ..models.user import User
from ..models.tag import Tag
from ..models.task_tag import TaskTag
from ..api.schemas.task import TaskCreateRequest, TaskUpdateRequest
from ..core.exceptions import TaskNotFoundException, InsufficientPermissionException, UserNotFoundException


class TaskService:
    """
    Service class to handle task-related business logic.
    """

    @staticmethod
    def create_task(session: Session, task_create: 'TaskCreateRequest', user_id: UUID) -> dict:
        """
        Create a new task for the given user.
        """
        # Create a new task instance with the provided data and user_id
        db_task = Task(
            title=task_create.title,
            description=task_create.description,
            completed=task_create.completed,
            user_id=user_id,
            priority=task_create.priority,
            due_date=task_create.due_date,
            reminder_time=task_create.reminder_time,
            recurrence_type=task_create.recurrence_type,
            recurrence_metadata=task_create.recurrence_metadata
        )

        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        # Return a dictionary representation of the created task
        return {
            "id": str(db_task.id),
            "title": db_task.title,
            "description": db_task.description,
            "completed": db_task.completed,
            "user_id": str(db_task.user_id),
            "created_at": db_task.created_at,
            "updated_at": db_task.updated_at,
            "priority": db_task.priority,
            "due_date": db_task.due_date,
            "reminder_time": db_task.reminder_time,
            "recurrence_type": db_task.recurrence_type,
            "recurrence_metadata": db_task.recurrence_metadata
        }

    @staticmethod
    def get_task_by_id(session: Session, task_id: UUID, user_id: UUID) -> Optional[dict]:
        """
        Get a specific task by ID for the given user.
        """
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(statement).first()

        if not task:
            raise TaskNotFoundException(task_id)

        # Get tags associated with the task
        # We need to query the association table to get the tags
        task_tags_statement = select(Tag).join(TaskTag).where(
            TaskTag.task_id == task.id
        )
        tags = session.exec(task_tags_statement).all()

        return {
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
        }

    @staticmethod
    def get_tasks_by_user(session: Session, user_id: UUID) -> List[dict]:
        """
        Get all tasks for the given user.
        """
        statement = select(Task).where(Task.user_id == user_id)
        tasks = session.exec(statement).all()

        result = []
        for task in tasks:
            # Get tags associated with each task
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

    @staticmethod
    def update_task(session: Session, task_id: UUID, task_update: 'TaskUpdateRequest', user_id: UUID = None) -> Optional[dict]:
        """
        Update a specific task for the given user.
        """
        statement = select(Task).where(Task.id == task_id)
        if user_id:
            statement = statement.where(Task.user_id == user_id)
        db_task = session.exec(statement).first()

        if not db_task:
            raise TaskNotFoundException(task_id)

        # Update only the fields that are provided
        if task_update.title is not None:
            db_task.title = task_update.title
        if task_update.description is not None:
            db_task.description = task_update.description
        if task_update.completed is not None:
            db_task.completed = task_update.completed
        if task_update.priority is not None:
            db_task.priority = task_update.priority
        if task_update.due_date is not None:
            db_task.due_date = task_update.due_date
        if task_update.reminder_time is not None:
            db_task.reminder_time = task_update.reminder_time
        if task_update.recurrence_type is not None:
            db_task.recurrence_type = task_update.recurrence_type
        if task_update.recurrence_metadata is not None:
            db_task.recurrence_metadata = task_update.recurrence_metadata

        db_task.updated_at = datetime.datetime.utcnow()
        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        # Get tags associated with the task
        task_tags_statement = select(Tag).join(TaskTag).where(
            TaskTag.task_id == db_task.id
        )
        tags = session.exec(task_tags_statement).all()

        return {
            "id": str(db_task.id),
            "title": db_task.title,
            "description": db_task.description,
            "completed": db_task.completed,
            "user_id": str(db_task.user_id),
            "created_at": db_task.created_at,
            "updated_at": db_task.updated_at,
            "priority": db_task.priority,
            "due_date": db_task.due_date,
            "reminder_time": db_task.reminder_time,
            "recurrence_type": db_task.recurrence_type,
            "recurrence_metadata": db_task.recurrence_metadata,
            "tags": [{"id": tag.id, "name": tag.name} for tag in tags]
        }

    @staticmethod
    def delete_task(session: Session, task_id: UUID, user_id: UUID) -> bool:
        """
        Delete a specific task.
        """
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        db_task = session.exec(statement).first()

        if not db_task:
            raise TaskNotFoundException(task_id)

        session.delete(db_task)
        session.commit()

        return True

    @staticmethod
    def toggle_task_completion(session: Session, task_id: UUID, user_id: UUID) -> Optional[dict]:
        """
        Toggle the completion status of a specific task for the given user.
        """
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        db_task = session.exec(statement).first()

        if not db_task:
            raise TaskNotFoundException(task_id)

        # Toggle the completion status
        db_task.completed = not db_task.completed

        # Handle recurrence logic if the task is being completed and has recurrence
        if db_task.completed and db_task.recurrence_type:
            TaskService._create_next_recurrence(session, db_task)

        db_task.updated_at = datetime.datetime.utcnow()

        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        # Get tags associated with the task
        task_tags_statement = select(Tag).join(TaskTag).where(
            TaskTag.task_id == db_task.id
        )
        tags = session.exec(task_tags_statement).all()

        return {
            "id": str(db_task.id),
            "title": db_task.title,
            "description": db_task.description,
            "completed": db_task.completed,
            "user_id": str(db_task.user_id),
            "created_at": db_task.created_at,
            "updated_at": db_task.updated_at,
            "priority": db_task.priority,
            "due_date": db_task.due_date,
            "reminder_time": db_task.reminder_time,
            "recurrence_type": db_task.recurrence_type,
            "recurrence_metadata": db_task.recurrence_metadata,
            "tags": [{"id": tag.id, "name": tag.name} for tag in tags]
        }

    @staticmethod
    def _create_next_recurrence(session: Session, completed_task: Task) -> Optional[Task]:
        """
        Create the next occurrence of a recurring task when the current one is completed.
        """
        if not completed_task.recurrence_type:
            return None

        # Calculate next occurrence date based on recurrence type
        next_due_date = TaskService._calculate_next_occurrence(
            completed_task.due_date,
            completed_task.recurrence_type
        )

        if next_due_date:
            # Create a new task with the same properties but for the next occurrence
            new_task = Task(
                title=completed_task.title,
                description=completed_task.description,
                completed=False,
                user_id=completed_task.user_id,
                priority=completed_task.priority,
                due_date=next_due_date,
                reminder_time=completed_task.reminder_time,  # Keep the same reminder time
                recurrence_type=completed_task.recurrence_type,
                recurrence_metadata=completed_task.recurrence_metadata
            )

            session.add(new_task)
            session.commit()
            session.refresh(new_task)

            # Copy tags to the new task
            TaskService._copy_tags_to_task(session, completed_task.id, new_task.id)

            return new_task

        return None

    @staticmethod
    def _calculate_next_occurrence(current_due_date: Optional[datetime.datetime],
                                recurrence_type: str) -> Optional[datetime.datetime]:
        """
        Calculate the next occurrence date based on the recurrence type.
        """
        if not current_due_date:
            return None

        if recurrence_type == "daily":
            return current_due_date + datetime.timedelta(days=1)
        elif recurrence_type == "weekly":
            return current_due_date + datetime.timedelta(weeks=1)
        elif recurrence_type == "monthly":
            # Handle month overflow
            current_month = current_due_date.month
            current_year = current_due_date.year
            next_month = current_month + 1
            next_year = current_year

            if next_month > 12:
                next_month = 1
                next_year += 1

            # Handle days that don't exist in all months (e.g., Jan 31 -> Feb 31 doesn't exist)
            next_day = current_due_date.day
            max_day_in_next_month = TaskService._get_max_day_for_month(next_year, next_month)
            if next_day > max_day_in_next_month:
                next_day = max_day_in_next_month

            return current_due_date.replace(year=next_year, month=next_month, day=next_day)
        else:
            # Unknown recurrence type
            return None

    @staticmethod
    def _get_max_day_for_month(year: int, month: int) -> int:
        """
        Get the maximum number of days for a given month and year.
        """
        import calendar
        return calendar.monthrange(year, month)[1]

    @staticmethod
    def _copy_tags_to_task(session: Session, source_task_id: UUID, target_task_id: UUID):
        """
        Copy tags from one task to another.
        """
        # Get tags from the source task
        source_tags_statement = select(Tag).join(TaskTag).where(
            TaskTag.task_id == source_task_id
        )
        source_tags = session.exec(source_tags_statement).all()

        # Add each tag to the target task
        for tag in source_tags:
            # Check if the association already exists to avoid duplicates
            existing_assoc = session.exec(
                select(TaskTag).where(
                    TaskTag.task_id == target_task_id,
                    TaskTag.tag_id == tag.id
                )
            ).first()

            if not existing_assoc:
                # Add the tag to the new task
                session.execute(
                    TaskTag.insert().values(
                        task_id=target_task_id,
                        tag_id=tag.id
                    )
                )

    @staticmethod
    def search_tasks(session: Session, user_id: UUID, search_query: Optional[str] = None,
                     status: Optional[bool] = None, priority: Optional[str] = None,
                     tag_names: Optional[List[str]] = None,
                     due_date_from: Optional[datetime.datetime] = None,
                     due_date_to: Optional[datetime.datetime] = None,
                     sort_by: Optional[str] = None,
                     sort_order: Optional[str] = "asc") -> List[dict]:
        """
        Search and filter tasks based on various criteria.
        """
        # Start with the basic query
        statement = select(Task).where(Task.user_id == user_id)

        # Apply search filter (search in title and description)
        if search_query:
            search_filter = Task.title.ilike(f"%{search_query}%") | Task.description.ilike(f"%{search_query}%")
            statement = statement.where(search_filter)

        # Apply status filter
        if status is not None:
            statement = statement.where(Task.completed == status)

        # Apply priority filter
        if priority:
            statement = statement.where(Task.priority == priority)

        # Apply due date range filter
        if due_date_from:
            statement = statement.where(Task.due_date >= due_date_from)
        if due_date_to:
            statement = statement.where(Task.due_date <= due_date_to)

        # Apply sorting
        if sort_by == "priority":
            if sort_order == "desc":
                statement = statement.order_by(Task.priority.desc())
            else:
                statement = statement.order_by(Task.priority.asc())
        elif sort_by == "due_date":
            if sort_order == "desc":
                statement = statement.order_by(Task.due_date.desc())
            else:
                statement = statement.order_by(Task.due_date.asc())
        elif sort_by == "created_date":
            if sort_order == "desc":
                statement = statement.order_by(Task.created_at.desc())
            else:
                statement = statement.order_by(Task.created_at.asc())
        elif sort_by == "title":
            if sort_order == "desc":
                statement = statement.order_by(Task.title.desc())
            else:
                statement = statement.order_by(Task.title.asc())
        else:
            # Default sorting by creation date (newest first)
            statement = statement.order_by(Task.created_at.desc())

        tasks = session.exec(statement).all()

        result = []
        for task in tasks:
            # Get tags associated with each task
            task_tags_statement = select(Tag).join(TaskTag).where(
                TaskTag.task_id == task.id
            )
            tags = session.exec(task_tags_statement).all()

            # Apply tag filter after query (since tags are in a separate table)
            if tag_names and not any(tag.name in tag_names for tag in tags):
                continue

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