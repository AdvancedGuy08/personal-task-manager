from typing import Any
from pydantic import BaseModel
from sqlalchemy import delete, insert
from sqlalchemy.ext.asyncio import AsyncSession

from abc import ABC

from schemas import Pagination


class AbstractRepository(ABC):
    def __init__(self, session: AsyncSession):
        super().__init__()
        self.session = session

    async def get_all(self, pagination: Pagination):
        raise NotImplementedError

    async def get_one(self, id: int):
        raise NotImplementedError

    async def add_one(self, data: BaseModel) -> int:
        raise NotImplementedError

    async def delete(self, id: int) -> None:
        raise NotImplementedError


class Repository(AbstractRepository):
    model = None

    async def _get_one(self, id: int) -> Any | None:
        return await self.session.get(self.model, id)

    async def add_one(self, data: BaseModel) -> int:
        stmt = insert(self.model).values(**data.model_dump()).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def delete(self, id: int) -> None:
        stmt = delete(self.model).where(self.model.id == id)
        await self.session.execute(stmt)
