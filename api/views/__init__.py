from fastapi import FastAPI

from .users import users as users_router


def include_routers(app: FastAPI) -> None:
    app.include_router(users_router)
