from fastapi import APIRouter, Depends, HTTPException

from app.api.v1.dependencies import get_user_service
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserRead, status_code=201)
async def create_user(
    data: UserCreate,
    service: UserService = Depends(get_user_service),
) -> UserRead:
    try:
        user = await service.register(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return UserRead.model_validate(user)


@router.get("/{user_id}", response_model=UserRead)
async def read_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
) -> UserRead:
    user = await service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserRead.model_validate(user)


@router.get("/", response_model=list[UserRead])
async def list_users(
    service: UserService = Depends(get_user_service),
) -> list[UserRead]:
    users = await service.list_users()
    return [UserRead.model_validate(u) for u in users]
