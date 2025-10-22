from datetime import datetime
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_async_session
from repositories import ProjectRepository, UserRepository
import schemas
from services import ProjectService, UserService


PaginationDep = Annotated[schemas.Pagination, Depends()]
SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


def get_user_repository(session: SessionDep):
    return UserRepository(session)


UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]


def get_user_service(user_repo: UserRepositoryDep):
    return UserService(user_repo)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
UserDataCreateDep = Annotated[schemas.UserCreate, Depends()]


def get_project_repository(session: SessionDep):
    return ProjectRepository(session)


ProjectRepoDep = Annotated[ProjectRepository, Depends(get_project_repository)]


def get_project_service(project_repo: ProjectRepoDep):
    return ProjectService(project_repo)


ProjectServiceDep = Annotated[ProjectService, Depends(get_project_service)]
ProjectDataCreateDep = Annotated[schemas.ProjectCreate, Depends()]


def get_current_user():
    return schemas.User(
        created_at=datetime.now(),
        email="crutch@email.com",
        first_name="Crutch",
        username="crutch",
        id=1,
        is_active=True,
        updated_at=datetime.now(),
    )


CurrentUserDep = Annotated[schemas.User, Depends(get_current_user)]
