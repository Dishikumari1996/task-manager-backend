# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session

# from app.db.database import get_db
# from app.models.task import Task
# from app.schemas.task import TaskCreate, TaskResponse
# from app.services.auth_dependency import get_current_user

# router = APIRouter(prefix="/tasks", tags=["Tasks"])

# @router.post("/", response_model=TaskResponse)
# def create_task(
#     task: TaskCreate,
#     db: Session = Depends(get_db),
#     current_user: dict = Depends(get_current_user)
# ):
#     new_task = Task(
#         title=task.title,
#         description=task.description,
#         user_id=current_user["user_id"]
#     )

#     db.add(new_task)
#     db.commit()
#     db.refresh(new_task)

#     return new_task

# @router.get("/", response_model=list[TaskResponse])
# def get_tasks(
#     skip: int = 0,
#     limit: int = 10,
#     status: str = None,
#     priority: str = None,
#     db: Session = Depends(get_db),
#     current_user: dict = Depends(get_current_user)
# ):
#     query = db.query(Task).filter(Task.user_id == current_user["user_id"])

#     if status:
#         query = query.filter(Task.status == status)

#     if priority:
#         query = query.filter(Task.priority == priority)

#     return query.offset(skip).limit(limit).all()

# @router.put("/{task_id}", response_model=TaskResponse)
# def update_task(
#     task_id: int,
#     task: TaskCreate,
#     db: Session = Depends(get_db),
#     current_user: dict = Depends(get_current_user)
# ):
#     existing_task = db.query(Task).filter(Task.id == task_id).first()

#     if not existing_task:
#         raise HTTPException(status_code=404, detail="Task not found")

#     # 🔐 ownership check
#     if existing_task.user_id != current_user["user_id"]:
#         raise HTTPException(status_code=403, detail="Not allowed")

#     existing_task.title = task.title
#     existing_task.description = task.description

#     db.commit()
#     db.refresh(existing_task)

#     return existing_task

# @router.delete("/{task_id}")
# def delete_task(
#     task_id: int,
#     db: Session = Depends(get_db),
#     current_user: dict = Depends(get_current_user)
# ):
#     task = db.query(Task).filter(Task.id == task_id).first()

#     if not task:
#         raise HTTPException(status_code=404, detail="Task not found")

#     if task.user_id != current_user["user_id"]:
#         raise HTTPException(status_code=403, detail="Not allowed")

#     db.delete(task)
#     db.commit()

#     return {"message": "Task deleted successfully"}

# @router.patch("/{task_id}/status", response_model=TaskResponse)
# def update_task_status(
#     task_id: int,
#     status: str,
#     db: Session = Depends(get_db),
#     current_user: dict = Depends(get_current_user)
# ):
#     task = db.query(Task).filter(Task.id == task_id).first()

#     if not task:
#         raise HTTPException(status_code=404, detail="Task not found")

#     if task.user_id != current_user["user_id"]:
#         raise HTTPException(status_code=403, detail="Not allowed")

#     valid_status = ["todo", "in-progress", "done"]

#     if status not in valid_status:
#         raise HTTPException(status_code=400, detail="Invalid status")

#     task.status = status
#     db.commit()
#     db.refresh(task)

#     return task

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.task import TaskCreate
from app.schemas.response import APIResponse
from app.services.auth_dependency import get_current_user
from app.services import task_service

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=APIResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return task_service.create_task(db, task, current_user["user_id"])


@router.get("/", response_model=APIResponse)
def get_tasks(skip: int = 0, limit: int = 10, status: str = None, priority: str = None,
              db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return task_service.get_tasks(db, current_user["user_id"], skip, limit, status, priority)


@router.put("/{task_id}", response_model=APIResponse)
def update_task(task_id: int, task: TaskCreate, db: Session = Depends(get_db),
                current_user: dict = Depends(get_current_user)):
    return task_service.update_task(db, task_id, task, current_user["user_id"])


@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return task_service.delete_task(db, task_id, current_user["user_id"])


@router.patch("/{task_id}/status", response_model=APIResponse)
def update_status(task_id: int, status: str, db: Session = Depends(get_db),
                  current_user: dict = Depends(get_current_user)):
    return task_service.update_task_status(db, task_id, status, current_user["user_id"])