from sqlalchemy import select
from sqlalchemy.orm import joinedload
from models import Project as ProjectModel
import schemas
from utils.repository import Repository


class ProjectRepository(Repository):
    model = ProjectModel

    async def get_all(self, pagination: schemas.Pagination):
        stmt = (
            select(self.model)
            .limit(pagination.limit)
            .offset(pagination.limit * pagination.offset)
            .options(joinedload(self.model.owner))
        )
        res = await self.session.execute(stmt)

        return [
            schemas.ProjectWithOwner.model_validate(instance, from_attributes=True)
            for instance in res.unique().scalars().all()
        ]

    async def get_one(self, id: int) -> schemas.Project | None:
        project = await self._get_one(id)
        if project is not None:
            return schemas.Project.model_validate(project, from_attributes=True)
