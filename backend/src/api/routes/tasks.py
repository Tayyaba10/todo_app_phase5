from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from uuid import UUID
from ..deps import get_current_user
from ..schemas.task import TaskCreateRequest, TaskResponse, TaskListResponse, TaskUpdateRequest, TaskToggleCompleteRequest, MessageResponse
from ...services.task_service import TaskService
from ...models.task import Task
from ...core.database import get_session
from ...core.exceptions import TaskNotFoundException, InsufficientPermissionException


router = APIRouter()


@router.get("/", response_model=TaskListResponse)
def list_tasks(
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session),
    search: str = None,
    status: bool = None,
    priority: str = None,
    tags: str = None,  # Comma-separated tag names
    due_date_from: str = None,
    due_date_to: str = None,
    sort_by: str = None,  # created_date, due_date, priority, title
    sort_order: str = "desc"  # asc or desc
):
    """
    Get all tasks for the authenticated user with optional search, filter, and sort.
    """
    user_id = current_user["user_id"]

    # Parse tags if provided
    tag_list = None
    if tags:
        tag_list = [tag.strip() for tag in tags.split(',')]

    # Parse date range if provided
    from datetime import datetime
    parsed_due_date_from = None
    parsed_due_date_to = None

    if due_date_from:
        parsed_due_date_from = datetime.fromisoformat(due_date_from.replace('Z', '+00:00'))
    if due_date_to:
        parsed_due_date_to = datetime.fromisoformat(due_date_to.replace('Z', '+00:00'))

    # Use search functionality if any filters are provided
    if search or status is not None or priority or tag_list or parsed_due_date_from or parsed_due_date_to:
        tasks = TaskService.search_tasks(
            session=session,
            user_id=user_id,
            search_query=search,
            status=status,
            priority=priority,
            tag_names=tag_list,
            due_date_from=parsed_due_date_from,
            due_date_to=parsed_due_date_to,
            sort_by=sort_by,
            sort_order=sort_order
        )
    else:
        # If no filters, just get all tasks
        tasks = TaskService.get_tasks_by_user(session=session, user_id=user_id)

    task_responses = []
    for task in tasks:
        # Create tag response objects
        tag_responses = [
            {"id": tag_data["id"], "name": tag_data["name"]}
            for tag_data in task.get("tags", [])
        ]

        task_responses.append(
            TaskResponse(
                id=task["id"],
                title=task["title"],
                description=task["description"],
                completed=task["completed"],
                user_id=task["user_id"],
                created_at=task["created_at"],
                updated_at=task["updated_at"],
                priority=task["priority"],
                due_date=task["due_date"],
                reminder_time=task["reminder_time"],
                recurrence_type=task["recurrence_type"],
                recurrence_metadata=task["recurrence_metadata"],
                tags=tag_responses
            )
        )

    return TaskListResponse(tasks=task_responses)


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_create: TaskCreateRequest,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user.
    """
    user_id = current_user["user_id"]

    # Validate reminder time if provided
    if task_create.reminder_time and task_create.due_date:
        from ...services.reminder_service import ReminderService
        if not ReminderService.validate_reminder_time(task_create.reminder_time, task_create.due_date):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Reminder time must be before due date and in the future"
            )
    elif task_create.reminder_time:
        from ...services.reminder_service import ReminderService
        if not ReminderService.validate_reminder_time(task_create.reminder_time):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Reminder time must be in the future"
            )

    # Create the task using the service
    db_task = TaskService.create_task(
        session=session,
        task_create=task_create,
        user_id=user_id
    )

    # Create tag response objects
    tag_responses = [
        {"id": tag_data["id"], "name": tag_data["name"]}
        for tag_data in db_task.get("tags", [])
    ]

    # Return the created task
    return TaskResponse(
        id=db_task["id"],
        title=db_task["title"],
        description=db_task["description"],
        completed=db_task["completed"],
        user_id=db_task["user_id"],
        created_at=db_task["created_at"],
        updated_at=db_task["updated_at"],
        priority=db_task["priority"],
        due_date=db_task["due_date"],
        reminder_time=db_task["reminder_time"],
        recurrence_type=db_task["recurrence_type"],
        recurrence_metadata=db_task["recurrence_metadata"],
        tags=tag_responses
    )


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: UUID,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get a specific task by ID for the authenticated user.
    """
    user_id = current_user["user_id"]

    db_task = TaskService.get_task_by_id(session=session, task_id=task_id, user_id=user_id)

    # Create tag response objects
    tag_responses = [
        {"id": tag_data["id"], "name": tag_data["name"]}
        for tag_data in db_task.get("tags", [])
    ]

    return TaskResponse(
        id=db_task["id"],
        title=db_task["title"],
        description=db_task["description"],
        completed=db_task["completed"],
        user_id=db_task["user_id"],
        created_at=db_task["created_at"],
        updated_at=db_task["updated_at"],
        priority=db_task["priority"],
        due_date=db_task["due_date"],
        reminder_time=db_task["reminder_time"],
        recurrence_type=db_task["recurrence_type"],
        recurrence_metadata=db_task["recurrence_metadata"],
        tags=tag_responses
    )


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: UUID,
    task_update: TaskUpdateRequest,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update a specific task for the authenticated user.
    """
    user_id = current_user["user_id"]

    # Validate reminder time if provided
    if task_update.reminder_time is not None and (
        task_update.due_date is not None or
        TaskService.get_task_by_id(session, task_id, user_id).get("due_date") is not None
    ):
        # Get the current task to check its due_date if not provided in update
        current_task = TaskService.get_task_by_id(session, task_id, user_id)
        due_date = task_update.due_date or current_task.get("due_date")

        from ...services.reminder_service import ReminderService
        if not ReminderService.validate_reminder_time(task_update.reminder_time, due_date):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Reminder time must be before due date and in the future"
            )
    elif task_update.reminder_time:
        from ...services.reminder_service import ReminderService
        if not ReminderService.validate_reminder_time(task_update.reminder_time):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Reminder time must be in the future"
            )

    db_task = TaskService.update_task(
        session=session,
        task_id=task_id,
        task_update=task_update,
        user_id=user_id
    )

    # Create tag response objects
    tag_responses = [
        {"id": tag_data["id"], "name": tag_data["name"]}
        for tag_data in db_task.get("tags", [])
    ]

    return TaskResponse(
        id=db_task["id"],
        title=db_task["title"],
        description=db_task["description"],
        completed=db_task["completed"],
        user_id=db_task["user_id"],
        created_at=db_task["created_at"],
        updated_at=db_task["updated_at"],
        priority=db_task["priority"],
        due_date=db_task["due_date"],
        reminder_time=db_task["reminder_time"],
        recurrence_type=db_task["recurrence_type"],
        recurrence_metadata=db_task["recurrence_metadata"],
        tags=tag_responses
    )


@router.delete("/{task_id}", response_model=MessageResponse)
def delete_task(
    task_id: UUID,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a specific task for the authenticated user.
    """
    user_id = current_user["user_id"]

    success = TaskService.delete_task(session=session, task_id=task_id, user_id=user_id)

    if success:
        return MessageResponse(message="Task deleted successfully")
    else:
        raise HTTPException(status_code=404, detail="Task not found")


@router.patch("/{task_id}/complete", response_model=TaskResponse)
def toggle_task_completion(
    task_id: UUID,
    task_toggle: TaskToggleCompleteRequest,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Toggle the completion status of a specific task for the authenticated user.
    """
    user_id = current_user["user_id"]

    db_task = TaskService.toggle_task_completion(session=session, task_id=task_id, user_id=user_id)

    # Create tag response objects
    tag_responses = [
        {"id": tag_data["id"], "name": tag_data["name"]}
        for tag_data in db_task.get("tags", [])
    ]

    return TaskResponse(
        id=db_task["id"],
        title=db_task["title"],
        description=db_task["description"],
        completed=db_task["completed"],
        user_id=db_task["user_id"],
        created_at=db_task["created_at"],
        updated_at=db_task["updated_at"],
        priority=db_task["priority"],
        due_date=db_task["due_date"],
        reminder_time=db_task["reminder_time"],
        recurrence_type=db_task["recurrence_type"],
        recurrence_metadata=db_task["recurrence_metadata"],
        tags=tag_responses
    )