from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


def get_task(db: Session, task_id: int) -> Task | None:
    return db.get(Task, task_id)


def get_tasks(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    owner_id: int | None = None,
    is_completed: bool | None = None,
) -> list[Task]:
    stmt = select(Task)
    if owner_id is not None:
        stmt = stmt.where(Task.owner_id == owner_id)
    if is_completed is not None:
        stmt = stmt.where(Task.is_completed == is_completed)
    stmt = stmt.offset(skip).limit(limit)
    return list(db.scalars(stmt).all())


def create_task(db: Session, task_in: TaskCreate) -> Task:
    db_task = Task(**task_in.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, db_task: Task, task_in: TaskUpdate) -> Task:
    update_data = task_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)

    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, db_task: Task) -> None:
    db.delete(db_task)
    db.commit()