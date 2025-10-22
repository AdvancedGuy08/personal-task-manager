from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_async_session
from repositories import UserRepository
from schemas.pagination import Pagination
from schemas.users import UserCreate
from services import UserService


PaginationDep = Annotated[Pagination, Depends()]
SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


def get_user_repository(session: SessionDep):
    return UserRepository(session)


UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]


def get_user_service(user_repo: UserRepositoryDep):
    return UserService(user_repo)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
UserDataCreateDep = Annotated[UserCreate, Depends()]
