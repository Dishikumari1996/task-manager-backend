from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.task import Task
from app.schemas.response import APIResponse
from app.schemas.task import TaskResponse

def create_task(db: Session, task_data, user_id: int):
    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        user_id=user_id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return APIResponse(
        success=True,
        message="Task created",
        data=TaskResponse.model_validate(new_task)
    )

def get_tasks(db: Session, user_id: int, skip: int, limit: int, status=None, priority=None):
    query = db.query(Task).filter(Task.user_id == user_id)

    if status:
        query = query.filter(Task.status == status)

    if priority:
        query = query.filter(Task.priority == priority)

    # return query.offset(skip).limit(limit).all()
    tasks = query.offset(skip).limit(limit).all()
    return APIResponse(
        success=True,
        message="Tasks fetched",
        data=[TaskResponse.model_validate(task) for task in tasks]
    )

def update_task(db: Session, task_id: int, task_data, user_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not allowed")

    task.title = task_data.title
    task.description = task_data.description
    task.priority = task_data.priority

    db.commit()
    db.refresh(task)

    return APIResponse(
        success=True,
        message="Task updated",
        data=TaskResponse.model_validate(task)
    )

def delete_task(db: Session, task_id: int, user_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not allowed")

    db.delete(task)
    db.commit()

    return APIResponse(
        success=True,
        message="Task deleted successfully"
    )

def update_task_status(db: Session, task_id: int, status: str, user_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not allowed")

    valid_status = ["todo", "in-progress", "done"]

    if status not in valid_status:
        raise HTTPException(status_code=400, detail="Invalid status")

    task.status = status

    db.commit()
    db.refresh(task)

    return APIResponse(
        success=True,
        message="Task status updated",
        data=TaskResponse.model_validate(task)
    )