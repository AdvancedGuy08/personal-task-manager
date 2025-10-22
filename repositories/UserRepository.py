from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.pagination import Pagination
from schemas.users import (
    User as UserSchema,
    UserCreate as UserCreateSchema,
)
from models.users import User as UserModel


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, pagination: Pagination) -> list[UserSchema]:
        stmt = (
            select(UserModel)
            .limit(pagination.limit)
            .offset(pagination.limit * pagination.offset)
        )
        res = await self.session.execute(stmt)

        return [
            UserSchema.model_validate(instance, from_attributes=True)
            for instance in res.scalars().all()
        ]

    async def get_one(self, id: int) -> UserSchema | None:
        stmt = select(UserModel).where(UserModel.id == id)
        res = await self.session.execute(stmt)
        user = res.scalar()
        if user is not None:
            return UserSchema.model_validate(user, from_attributes=True)

    async def add_one(self, data: UserCreateSchema) -> int:
        stmt = insert(UserModel).values(**data.model_dump()).returning(UserModel.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def delete(self, id: int) -> None:
        stmt = delete(UserModel).where(UserModel.id == id)
        await self.session.execute(stmt)
