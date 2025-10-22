from contextlib import asynccontextmanager
from fastapi import FastAPI

from api.views import include_routers
from core.database import Base, async_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # async with async_engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
    #     print("База создана")
    yield
    # async with async_engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)
    #     print("База очищена")


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    include_routers(app)

    return app


app = create_app()
