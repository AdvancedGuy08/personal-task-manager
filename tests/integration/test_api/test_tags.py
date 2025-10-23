import pytest
from httpx import AsyncClient


class TestTagsAPI:
    async def test_create_tag(self, client: AsyncClient):
        """Тест создания тега"""
        tag_data = {"name": "важный", "color": "FF5733"}

        response = await client.post("/api/tags", json=tag_data)

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "важный"
        assert data["color"] == "FF5733"
        assert "id" in data

    async def test_get_tags(self, client: AsyncClient, test_tag):
        """Тест получения списка тегов"""
        response = await client.get("/api/tags")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "test-tag"

    async def test_get_tag_by_id(self, client: AsyncClient, test_tag):
        """Тест получения тега по ID"""
        response = await client.get(f"/api/tags/{test_tag.id}")

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "test-tag"
        assert data["id"] == test_tag.id

    async def test_delete_tag(self, client: AsyncClient, test_tag):
        """Тест удаления тега"""
        response = await client.delete(f"/api/tags/{test_tag.id}")

        assert response.status_code == 200

        get_response = await client.get(f"/api/tags/{test_tag.id}")
        assert get_response.status_code == 404
