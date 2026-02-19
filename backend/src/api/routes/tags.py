from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from uuid import UUID
from ..deps import get_current_user
from ..schemas.task import TaskResponse, TagResponse
from ...services.tag_service import TagService
from ...services.task_service import TaskService
from ...models.tag import TagCreate
from ...core.database import get_session


router = APIRouter()


@router.get("/", response_model=List[TagResponse])
def list_tags(
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all tags.
    """
    tags = TagService.get_all_tags(session=session)
    return tags


@router.post("/{task_id}/tags/{tag_name}", response_model=TaskResponse)
def assign_tag_to_task(
    task_id: UUID,
    tag_name: str,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Assign a tag to a task. Creates the tag if it doesn't exist.
    """
    user_id = current_user["user_id"]

    # Verify that the task belongs to the user
    task = TaskService.get_task_by_id(session=session, task_id=task_id, user_id=user_id)

    success = TagService.assign_tag_to_task(session=session, task_id=task_id, tag_name=tag_name)

    if not success:
        raise HTTPException(status_code=400, detail="Failed to assign tag to task")

    # Return the updated task
    updated_task = TaskService.get_task_by_id(session=session, task_id=task_id, user_id=user_id)

    # Create tag response objects
    tag_responses = [
        {"id": tag_data["id"], "name": tag_data["name"]}
        for tag_data in updated_task.get("tags", [])
    ]

    return TaskResponse(
        id=updated_task["id"],
        title=updated_task["title"],
        description=updated_task["description"],
        completed=updated_task["completed"],
        user_id=updated_task["user_id"],
        created_at=updated_task["created_at"],
        updated_at=updated_task["updated_at"],
        priority=updated_task["priority"],
        due_date=updated_task["due_date"],
        reminder_time=updated_task["reminder_time"],
        recurrence_type=updated_task["recurrence_type"],
        recurrence_metadata=updated_task["recurrence_metadata"],
        tags=tag_responses
    )


@router.delete("/{task_id}/tags/{tag_id}", response_model=TaskResponse)
def remove_tag_from_task(
    task_id: UUID,
    tag_id: int,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Remove a tag from a task.
    """
    user_id = current_user["user_id"]

    # Verify that the task belongs to the user
    task = TaskService.get_task_by_id(session=session, task_id=task_id, user_id=user_id)

    success = TagService.remove_tag_from_task(session=session, task_id=task_id, tag_id=tag_id)

    if not success:
        raise HTTPException(status_code=400, detail="Failed to remove tag from task")

    # Return the updated task
    updated_task = TaskService.get_task_by_id(session=session, task_id=task_id, user_id=user_id)

    # Create tag response objects
    tag_responses = [
        {"id": tag_data["id"], "name": tag_data["name"]}
        for tag_data in updated_task.get("tags", [])
    ]

    return TaskResponse(
        id=updated_task["id"],
        title=updated_task["title"],
        description=updated_task["description"],
        completed=updated_task["completed"],
        user_id=updated_task["user_id"],
        created_at=updated_task["created_at"],
        updated_at=updated_task["updated_at"],
        priority=updated_task["priority"],
        due_date=updated_task["due_date"],
        reminder_time=updated_task["reminder_time"],
        recurrence_type=updated_task["recurrence_type"],
        recurrence_metadata=updated_task["recurrence_metadata"],
        tags=tag_responses
    )


@router.get("/{tag_id}/tasks", response_model=List[TaskResponse])
def get_tasks_by_tag(
    tag_id: int,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all tasks associated with a specific tag.
    """
    user_id = current_user["user_id"]

    tasks = TagService.get_tasks_by_tag(session=session, tag_id=tag_id)

    # Filter tasks to only include those belonging to the current user
    user_tasks = []
    for task in tasks:
        if str(task["user_id"]) == user_id:
            # Create tag response objects
            tag_responses = [
                {"id": tag_data["id"], "name": tag_data["name"]}
                for tag_data in task.get("tags", [])
            ]

            user_tasks.append(
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

    return user_tasks