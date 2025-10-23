import asyncio
from datetime import datetime
import pytest_asyncio
from typing import AsyncGenerator, Generator
import pytest
from sqlalchemy import StaticPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from httpx import ASGITransport, AsyncClient

from api.dependencies import get_current_user
from core.database import Base, get_async_session
from main import create_app
import schemas

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Event loop для всей сессии тестов"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def test_engine():
    """Создает тестовую базу данных для каждого теста"""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
        echo=False,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def test_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Создает тестовую сессию базы данных."""
    async_session = async_sessionmaker(test_engine, expire_on_commit=False)

    async with async_session() as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def client(test_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Создает тестовый клиент FastAPI"""
    app = create_app()

    def override_get_async_session():
        return test_session

    def override_get_current_user():
        return schemas.User(
            created_at=datetime.now(),
            email="test@example.com",
            first_name="Test",
            username="testuser",
            id=1,
            is_active=True,
            updated_at=datetime.now(),
        )

    app.dependency_overrides[get_async_session] = override_get_async_session
    app.dependency_overrides[get_current_user] = override_get_current_user

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest_asyncio.fixture(scope="function")
async def test_user(test_session: AsyncSession):
    """Создает тестового пользователя."""
    from models import User

    user = User(
        first_name="Test",
        last_name="User",
        username="testuser",
        email="test@example.com",
        is_active=True,
    )

    test_session.add(user)
    await test_session.commit()
    await test_session.refresh(user)

    return user


@pytest_asyncio.fixture(scope="function")
async def test_project(test_session: AsyncSession, test_user):
    """Создает тестовый проект."""
    from models import Project

    project = Project(name="Test Project", owner_id=test_user.id)

    test_session.add(project)
    await test_session.commit()
    await test_session.refresh(project)

    return project


@pytest_asyncio.fixture(scope="function")
async def test_tag(test_session: AsyncSession, test_user):
    """Создает тестовый тег."""
    from models import Tag

    tag = Tag(name="test-tag", color="FF5733", author_id=test_user.id)

    test_session.add(tag)
    await test_session.commit()
    await test_session.refresh(tag)

    return tag
