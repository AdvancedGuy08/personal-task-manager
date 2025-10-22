from fastapi import FastAPI

from .projects import projects as projects_router
from .users import users as users_router


def include_routers(app: FastAPI) -> None:
    app.include_router(projects_router)
    app.include_router(users_router)
