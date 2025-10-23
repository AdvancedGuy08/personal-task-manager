from typing import Iterable, Sequence
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from models import Tag
import schemas
from utils.repository import Repository


class TagRepository(Repository):
    model = Tag

    async def get_all(self, pagination: schemas.Pagination):
        stmt = (
            select(self.model)
            .limit(pagination.limit)
            .offset(pagination.limit * pagination.offset)
            .options(selectinload(self.model.projects))
        )
        res = await self.session.execute(stmt)

        return [
            schemas.TagWithRelations.model_validate(instance, from_attributes=True)
            for instance in res.unique().scalars().all()
        ]

    async def get_one(self, id: int) -> schemas.Tag | None:
        tag = await self._get_one(id)
        if tag is not None:
            return schemas.Tag.model_validate(tag, from_attributes=True)

    async def get_many(self, ids: Iterable[int]) -> list[schemas.Tag]:
        return [
            schemas.Tag.model_validate(tag, from_attributes=True)
            for tag in await self._get_many(ids)
        ]

    async def _get_many(self, ids: Iterable[int]) -> Sequence[Tag]:
        stmt = select(self.model).where(self.model.id.in_(ids))
        res = await self.session.execute(stmt)
        return res.scalars().all()
