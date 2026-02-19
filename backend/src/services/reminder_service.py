from sqlmodel import Session, select
from typing import List
from datetime import datetime, timedelta
from ..models.task import Task


class ReminderService:
    """
    Service class to handle reminder-related business logic.
    """

    @staticmethod
    def get_upcoming_reminders(session: Session,
                              time_window: timedelta = timedelta(minutes=30)) -> List[Task]:
        """
        Get tasks with reminders that are upcoming within the specified time window.

        Args:
            session: Database session
            time_window: Time window to check for upcoming reminders (default 30 minutes)

        Returns:
            List of tasks with upcoming reminders
        """
        now = datetime.utcnow()
        future_time = now + time_window

        # Find tasks with reminder_time between now and future_time
        statement = select(Task).where(
            Task.reminder_time >= now,
            Task.reminder_time <= future_time,
            Task.completed == False  # Only include non-completed tasks
        )

        upcoming_reminders = session.exec(statement).all()
        return upcoming_reminders

    @staticmethod
    def get_overdue_reminders(session: Session) -> List[Task]:
        """
        Get tasks with overdue reminders (reminders that should have triggered but haven't been handled).

        Args:
            session: Database session

        Returns:
            List of tasks with overdue reminders
        """
        now = datetime.utcnow()

        # Find tasks with reminder_time in the past and not completed
        statement = select(Task).where(
            Task.reminder_time < now,
            Task.completed == False,
            Task.reminder_time.is_not(None)  # Ensure reminder_time is not null
        )

        overdue_reminders = session.exec(statement).all()
        return overdue_reminders

    @staticmethod
    def get_tasks_with_reminders_for_user(session: Session, user_id) -> List[Task]:
        """
        Get all tasks with reminders for a specific user.

        Args:
            session: Database session
            user_id: ID of the user

        Returns:
            List of tasks with reminders for the user
        """
        statement = select(Task).where(
            Task.user_id == user_id,
            Task.reminder_time.is_not(None)  # Only tasks with reminders
        )

        tasks_with_reminders = session.exec(statement).all()
        return tasks_with_reminders

    @staticmethod
    def validate_reminder_time(reminder_time: datetime, due_date: datetime = None) -> bool:
        """
        Validate that the reminder time is before the due date (if provided) and in the future.

        Args:
            reminder_time: The time for the reminder
            due_date: Optional due date to compare against

        Returns:
            True if the reminder time is valid, False otherwise
        """
        now = datetime.utcnow()

        # Check if reminder is in the future
        if reminder_time <= now:
            return False

        # Check if reminder is before due date (if due date is provided)
        if due_date and reminder_time >= due_date:
            return False

        return True