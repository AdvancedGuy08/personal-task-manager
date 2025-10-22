from typing import Any
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from core.config import config

async_engine = create_async_engine(
    "postgresql+asyncpg://" + config.DATABASE_URL, echo=config.ECHO
)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_async_session():
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)

    def __repr__(self):
        def create_col_str(col: Any):
            return f"{col}={getattr(self, col)}"

        cols = [create_col_str(col) for col in self.__table__.columns.keys()]
        return f"<{self.__class__.__name__} {', '.join(cols)}>"
