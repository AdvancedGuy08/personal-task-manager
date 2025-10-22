from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

from ..dependencies import PaginationDep, UserDataCreateDep, UserServiceDep
from schemas.users import User

users = APIRouter(prefix="/api/users")


@users.get("", response_model=list[User])
async def get_users(pagination: PaginationDep, user_service: UserServiceDep):
    return await user_service.get_all(pagination)


@users.get("/{user_id}", response_model=User)
async def get_user(user_id: int, user_service: UserServiceDep):
    user = await user_service.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")
    return user


@users.post("", status_code=HTTP_201_CREATED)
async def create_user(data: UserDataCreateDep, user_service: UserServiceDep):
    return await user_service.add_one(data)


@users.delete("/{user_id}")
async def delete_user(user_id: int, user_service: UserServiceDep):
    return await user_service.delete(user_id)
