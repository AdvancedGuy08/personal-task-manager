from typing import Iterable
from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import joinedload, selectinload
from models import Project as ProjectModel, project_tag
import schemas
from utils.repository import Repository


class ProjectRepository(Repository):
    model = ProjectModel

    async def get_all(self, pagination: schemas.Pagination):
        stmt = (
            select(self.model)
            .limit(pagination.limit)
            .offset(pagination.limit * pagination.offset)
            .options(joinedload(self.model.owner), selectinload(self.model.tags))
        )
        res = await self.session.execute(stmt)

        return [
            schemas.ProjectWithRelations.model_validate(instance, from_attributes=True)
            for instance in res.unique().scalars().all()
        ]

    async def get_one(self, id: int) -> schemas.Project | None:
        project = await self._get_one(id)
        if project is not None:
            return schemas.Project.model_validate(project, from_attributes=True)

    async def update_name(self, id: int, name: str) -> None:
        stmt = (
            update(self.model)
            .where(self.model.id == id)
            .values({self.model.name: name})
        )
        await self.session.execute(stmt)

    async def add_tags_to_project(
        self, project_id: int, tags_ids: Iterable[int]
    ) -> None:
        project: ProjectModel | None = await self._get_one(project_id)
        if project is None:
            raise ValueError(f"Project with {project_id} not found")

        delete_stmt = delete(project_tag).where(
            project_tag.c["project_id"] == project_id
        )
        await self.session.execute(delete_stmt)

        insert_stmt = insert(project_tag).values(
            [{"project_id": project_id, "tag_id": tag_id} for tag_id in tags_ids]
        )
        await self.session.execute(insert_stmt)
