from uuid import uuid4

import pytest

from taskflow.exceptions import InvalidTokenError
from taskflow.jwt_token_service import JWTTokenService


def test_creates_and_decodes_access_token() -> None:
    token_service = JWTTokenService(
        secret="test-secret-bestehend-32-zeichen", access_token_expire_minutes=30
    )
    user_id = uuid4()
    token = token_service.create_access_token(user_id)
    decoded_user_id = token_service.decode_access_token(token)
    assert decoded_user_id == user_id


def test_raises_invalid_token_error_when_token_is_tampered() -> None:
    token_service = JWTTokenService(
        secret="test-secret-bestehend-32-zeichen",
        access_token_expire_minutes=30,
    )
    user_id = uuid4()
    token = token_service.create_access_token(user_id)
    tampered_token = token[:-1] + ("a" if token[-1] != "a" else "b")
    with pytest.raises(InvalidTokenError):
        token_service.decode_access_token(tampered_token)


def test_raises_invalid_token_error_when_token_is_expired() -> None:
    token_service = JWTTokenService(
        secret="test-secret-bestehend-aus-32-zeichen",
        access_token_expire_minutes=-1,
    )
    user_id = uuid4()
    token = token_service.create_access_token(user_id)
    with pytest.raises(InvalidTokenError):
        token_service.decode_access_token(token)
