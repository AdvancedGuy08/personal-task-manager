from repositories import UserRepository
import schemas


class UserService:
    def __init__(self, users_repo: UserRepository):
        self.users_repo = users_repo

    async def get_all(
        self, pagination: schemas.Pagination
    ) -> list[schemas.UserWithRelations]:
        return await self.users_repo.get_all(pagination)

    async def get_by_id(self, user_id: int) -> schemas.User | None:
        return await self.users_repo.get_one(user_id)

    async def add_one(self, data: schemas.UserCreate) -> int:
        return await self.users_repo.add_one(data)

    async def delete(self, user_id: int) -> None:
        return await self.users_repo.delete(user_id)
