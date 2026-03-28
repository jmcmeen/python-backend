from app.models.user import User
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate
from app.utils.hashing import hash_password


class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    async def register(self, data: UserCreate) -> User:
        existing = await self.repo.get_by_email(data.email)
        if existing:
            raise ValueError("A user with this email already exists")
        user = User(
            email=data.email,
            hashed_password=hash_password(data.password),
        )
        return await self.repo.create(user)

    async def get_user(self, user_id: int) -> User | None:
        return await self.repo.get_by_id(user_id)

    async def list_users(self) -> list[User]:
        return await self.repo.list_all()
