import pytest
from pydantic import ValidationError

from app.core.config import Settings


def test_secret_key_rejects_replace_with_placeholder():
    with pytest.raises(ValidationError, match="placeholder"):
        Settings(secret_key="replace-with-output-of-openssl-rand-hex-32")


def test_secret_key_rejects_change_me_placeholder():
    with pytest.raises(ValidationError, match="placeholder"):
        Settings(secret_key="change-me-in-production")


def test_secret_key_accepts_real_value():
    real = "3d8f9a2b4c1e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a"
    s = Settings(secret_key=real)
    assert s.secret_key.get_secret_value() == real


def test_secret_key_is_required_when_missing(monkeypatch):
    monkeypatch.delenv("SECRET_KEY", raising=False)
    with pytest.raises(ValidationError) as exc_info:
        Settings(_env_file=None)
    assert "secret_key" in str(exc_info.value).lower()
