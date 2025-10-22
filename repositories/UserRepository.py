from sqlalchemy import select
from sqlalchemy.orm import selectinload

import schemas
from models import User as UserModel
from utils.repository import Repository


class UserRepository(Repository):
    model = UserModel

    async def get_all(
        self, pagination: schemas.Pagination
    ) -> list[schemas.UserWithProjects]:
        stmt = (
            select(self.model)
            .options(selectinload(self.model.projects))
            .limit(pagination.limit)
            .offset(pagination.limit * pagination.offset)
        )
        res = await self.session.execute(stmt)

        return [
            schemas.UserWithProjects.model_validate(instance, from_attributes=True)
            for instance in res.unique().scalars().all()
        ]

    async def get_one(self, id: int) -> schemas.User | None:
        stmt = select(self.model).where(self.model.id == id)
        res = await self.session.execute(stmt)
        user = res.scalar()
        if user is not None:
            return schemas.User.model_validate(user, from_attributes=True)
