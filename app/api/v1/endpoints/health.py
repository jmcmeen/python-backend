from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

router = APIRouter(tags=["health"])

DbSession = Annotated[AsyncSession, Depends(get_db)]


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/ready")
async def ready(db: DbSession) -> dict[str, str]:
    try:
        await db.execute(text("SELECT 1"))
    except Exception as e:
        raise HTTPException(status_code=503, detail="database unavailable") from e
    return {"status": "ready"}
