import pytest
import pytest_asyncio

from app.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate
from app.services.user_service import UserService


@pytest_asyncio.fixture
async def service(db):
    repo = UserRepository(db)
    return UserService(repo)


@pytest.mark.asyncio
async def test_register_user(service):
    data = UserCreate(email="test@example.com", password="secret123")
    user = await service.register(data)
    assert user.email == "test@example.com"
    assert user.hashed_password != "secret123"
    assert user.is_active is True


@pytest.mark.asyncio
async def test_register_duplicate_email(service):
    data = UserCreate(email="dup@example.com", password="secret123")
    await service.register(data)
    with pytest.raises(ValueError, match="already exists"):
        await service.register(data)


@pytest.mark.asyncio
async def test_get_user(service):
    data = UserCreate(email="get@example.com", password="secret123")
    created = await service.register(data)
    found = await service.get_user(created.id)
    assert found is not None
    assert found.email == "get@example.com"


@pytest.mark.asyncio
async def test_list_users(service):
    await service.register(UserCreate(email="a@example.com", password="p"))
    await service.register(UserCreate(email="b@example.com", password="p"))
    users = await service.list_users()
    assert len(users) == 2
