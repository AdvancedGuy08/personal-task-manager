import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from repositories import ProjectRepository
import schemas


class TestProjectRepository:
    @pytest.fixture
    def project_repo(self, test_session: AsyncSession):
        """Создает экземпляр `ProjectRepository` для тестов"""
        return ProjectRepository(test_session)

    async def test_add_project(self, project_repo: ProjectRepository):
        """Тест добавления проекта в репозиторий"""
        project_data = schemas.ProjectCreateExtended(
            name="Репозиторий тест", owner_id=1
        )

        project_id = await project_repo.add_one(project_data)

        assert project_id is not None
        assert isinstance(project_id, int)

    async def test_get_project(self, project_repo: ProjectRepository, test_project):
        """Тест получения проекта из репозитория"""
        project = await project_repo.get_one(test_project.id)

        assert project is not None
        assert project.name == "Test Project"

    async def test_get_all_projects(
        self, project_repo: ProjectRepository, test_project
    ):
        """Тест получения всех проектов"""
        pagination = schemas.Pagination(limit=10, offset=0)
        projects = await project_repo.get_all(pagination)

        assert len(projects) == 1
        assert projects[0].name == "Test Project"
