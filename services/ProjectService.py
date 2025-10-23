from repositories import ProjectRepository
import schemas


class ProjectService:
    def __init__(self, project_repo: ProjectRepository):
        self.project_repo = project_repo

    async def get_all(
        self, pagination: schemas.Pagination
    ) -> list[schemas.ProjectWithRelations]:
        return await self.project_repo.get_all(pagination)

    async def get_by_id(self, project_id: int) -> schemas.Project | None:
        return await self.project_repo.get_one(project_id)

    async def add_one(self, data: schemas.ProjectCreateExtended) -> int:
        return await self.project_repo.add_one(data)

    async def delete(self, project_id: int) -> None:
        return await self.project_repo.delete(project_id)

    async def update(self, project_id: int, data: schemas.ProjectUpdate) -> None:
        data_dict = data.model_dump(exclude_unset=True)

        if "name" in data_dict:
            await self.project_repo.update_name(project_id, data_dict["name"])

        if "tags" in data_dict:
            await self._set_tags(project_id, data.tags)

    async def _set_tags(self, project_id: int, tags: list[schemas.Tag]) -> None:
        return await self.project_repo.add_tags_to_project(
            project_id, [tag.id for tag in tags]
        )
