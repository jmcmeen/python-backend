from datetime import UTC, datetime, timedelta
from typing import Any

import jwt

from app.core.config import settings

ALGORITHM = "HS256"


def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode["exp"] = expire
    return jwt.encode(to_encode, settings.secret_key.get_secret_value(), algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, settings.secret_key.get_secret_value(), algorithms=[ALGORITHM])
