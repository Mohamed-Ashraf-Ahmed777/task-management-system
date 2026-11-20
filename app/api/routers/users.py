from fastapi import APIRouter, HTTPException, status

from app.api.deps import CurrentUserDep, DbDep
from app.core.security import get_password_hash
from app.crud import user as user_crud
from app.schemas.user import UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserResponse])
def list_users(
    db: DbDep,
    current_user: CurrentUserDep,
    skip: int = 0,
    limit: int = 100,
):
    return user_crud.get_users(db, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(
    user_id: int,
    db: DbDep,
    current_user: CurrentUserDep,
):
    db_user = user_crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return db_user


@router.patch("/me", response_model=UserResponse)
def update_current_user(
    user_in: UserUpdate,
    db: DbDep,
    current_user: CurrentUserDep,
):
    if user_in.email is not None and str(user_in.email) != current_user.email:
        existing_user = user_crud.get_user_by_email(db, email=str(user_in.email))
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already registered",
            )

    hashed_password = (
        get_password_hash(user_in.password) if user_in.password is not None else None
    )
    return user_crud.update_user(
        db,
        db_user=current_user,
        user_in=user_in,
        hashed_password=hashed_password,
    )


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_current_user(
    db: DbDep,
    current_user: CurrentUserDep,
):
    user_crud.delete_user(db, db_user=current_user)