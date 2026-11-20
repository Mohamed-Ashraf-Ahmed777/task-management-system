from fastapi import APIRouter, HTTPException, status

from app.api.deps import CurrentUserDep, DbDep
from app.crud import task as task_crud
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_new_task(
    task_in: TaskCreate,
    db: DbDep,
    current_user: CurrentUserDep,
):
    task_data = task_in.model_copy(update={"owner_id": current_user.id})
    return task_crud.create_task(db, task_in=task_data)


@router.get("/", response_model=list[TaskResponse])
def list_my_tasks(
    db: DbDep,
    current_user: CurrentUserDep,
    skip: int = 0,
    limit: int = 100,
    is_completed: bool | None = None,
):
    return task_crud.get_tasks(
        db,
        skip=skip,
        limit=limit,
        owner_id=current_user.id,
        is_completed=is_completed,
    )


@router.get("/{task_id}", response_model=TaskResponse)
def get_task_by_id(
    task_id: int,
    db: DbDep,
    current_user: CurrentUserDep,
):
    db_task = task_crud.get_task(db, task_id=task_id)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    if db_task.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return db_task


@router.patch("/{task_id}", response_model=TaskResponse)
def update_existing_task(
    task_id: int,
    task_in: TaskUpdate,
    db: DbDep,
    current_user: CurrentUserDep,
):
    db_task = task_crud.get_task(db, task_id=task_id)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    if db_task.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return task_crud.update_task(db, db_task=db_task, task_in=task_in)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_task(
    task_id: int,
    db: DbDep,
    current_user: CurrentUserDep,
):
    db_task = task_crud.get_task(db, task_id=task_id)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    if db_task.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    task_crud.delete_task(db, db_task=db_task)