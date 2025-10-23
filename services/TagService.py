from repositories import TagRepository
import schemas


class TagService:
    def __init__(self, tag_repo: TagRepository):
        self.tag_repo = tag_repo

    async def get_all(
        self, pagination: schemas.Pagination
    ) -> list[schemas.TagWithRelations]:
        return await self.tag_repo.get_all(pagination)

    async def get_by_id(self, user_id: int) -> schemas.Tag | None:
        return await self.tag_repo.get_one(user_id)

    async def add_one(self, data: schemas.TagCreateExtended) -> int:
        return await self.tag_repo.add_one(data)

    async def delete(self, user_id: int) -> None:
        return await self.tag_repo.delete(user_id)
