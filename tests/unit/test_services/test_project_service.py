import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from repositories import ProjectRepository
from services import ProjectService
import schemas


class TestProjectService:
    @pytest.fixture
    def project_service(self, test_session: AsyncSession):
        """Создает экземпляр `ProjectService` для тестов"""
        project_repo = ProjectRepository(test_session)
        return ProjectService(project_repo)

    async def test_create_project(self, project_service: ProjectService):
        """Тест создания нового проекта через сервис"""
        project_data = schemas.ProjectCreateExtended(name="Тестовый проект", owner_id=1)

        project_id = await project_service.add_one(project_data)

        assert project_id is not None
        assert isinstance(project_id, int)

    async def test_get_project_by_id(
        self, project_service: ProjectService, test_project
    ):
        """Тест получения проекта по ID через сервис"""
        project = await project_service.get_by_id(test_project.id)

        assert project is not None
        assert project.name == "Test Project"
        assert project.id == test_project.id

    async def test_get_nonexistent_project(self, project_service: ProjectService):
        """Тест получения несуществующего проекта"""
        project = await project_service.get_by_id(999)

        assert project is None
