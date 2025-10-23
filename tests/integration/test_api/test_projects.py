from httpx import AsyncClient


class TestProjectAPI:
    async def test_create_project(self, client: AsyncClient):
        """Тест создания проекта"""
        project_data = {"name": "Новый проект"}

        response = await client.post("/api/projects", json=project_data)

        assert response.status_code == 201
        data = response.json()
        assert data == 1

    async def test_get_projects(self, client: AsyncClient, test_project):
        """Тест получения списка проектов"""
        response = await client.get("/api/projects")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Test Project"

    async def test_get_project_by_id(self, client: AsyncClient, test_project):
        """Тест получения проекта по ID"""
        response = await client.get(f"/api/projects/{test_project.id}")

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Project"
        assert data["id"] == test_project.id

    async def test_get_nonexistent_project(self, client: AsyncClient):
        """Тест получения несуществующего проекта"""
        response = await client.get("/api/projects/999")

        assert response.status_code == 404

    async def test_delete_project(self, client: AsyncClient, test_project):
        """Тест удаления проекта"""
        response = await client.delete(f"/api/projects/{test_project.id}")

        assert response.status_code == 200

        # Проверяем, что проект удален
        get_response = await client.get(f"/api/projects/{test_project.id}")
        assert get_response.status_code == 404

    async def test_update_project(self, client: AsyncClient, test_project):
        """Тест обновления проекта"""
        update_data = {"name": "Обновленный проект"}

        response = await client.patch(
            f"/api/projects/{test_project.id}", json=update_data
        )

        assert response.status_code == 200

        # Проверяем обновление
        get_response = await client.get(f"/api/projects/{test_project.id}")
        assert get_response.status_code == 200
        data = get_response.json()
        assert data["name"] == "Обновленный проект"
