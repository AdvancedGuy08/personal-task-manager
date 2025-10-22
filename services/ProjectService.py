from repositories import ProjectRepository
import schemas


class ProjectService:
    def __init__(self, project_repo: ProjectRepository):
        self.project_repo = project_repo

    async def get_all(
        self, pagination: schemas.Pagination
    ) -> list[schemas.ProjectWithOwner]:
        return await self.project_repo.get_all(pagination)

    async def get_by_id(self, user_id: int) -> schemas.Project | None:
        return await self.project_repo.get_one(user_id)

    async def add_one(self, data: schemas.ProjectCreateExtended) -> int:
        return await self.project_repo.add_one(data)

    async def delete(self, user_id: int) -> None:
        return await self.project_repo.delete(user_id)
