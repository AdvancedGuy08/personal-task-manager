from fastapi import APIRouter, HTTPException, status

from ..dependencies import PaginationDep, UserDataCreateDep, UserServiceDep
import schemas

users = APIRouter(prefix="/api/users", tags=["Users"])


@users.get("", response_model=list[schemas.UserWithProjects])
async def get_users(pagination: PaginationDep, user_service: UserServiceDep):
    return await user_service.get_all(pagination)


@users.get("/{user_id}", response_model=schemas.User)
async def get_user(user_id: int, user_service: UserServiceDep):
    user = await user_service.get_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@users.post("", status_code=status.HTTP_201_CREATED)
async def create_user(data: UserDataCreateDep, user_service: UserServiceDep):
    return await user_service.add_one(data)


@users.delete("/{user_id}")
async def delete_user(user_id: int, user_service: UserServiceDep):
    return await user_service.delete(user_id)
