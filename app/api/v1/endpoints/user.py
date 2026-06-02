from fastapi import APIRouter, HTTPException

from app.api.v1.dependencies import UserServiceDep
from app.schemas.user import UserCreate, UserRead

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserRead, status_code=201)
async def create_user(data: UserCreate, service: UserServiceDep) -> UserRead:
    try:
        user = await service.register(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    return UserRead.model_validate(user)


@router.get("/{user_id}", response_model=UserRead)
async def read_user(user_id: int, service: UserServiceDep) -> UserRead:
    user = await service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserRead.model_validate(user)


@router.get("/", response_model=list[UserRead])
async def list_users(service: UserServiceDep) -> list[UserRead]:
    users = await service.list_users()
    return [UserRead.model_validate(u) for u in users]
