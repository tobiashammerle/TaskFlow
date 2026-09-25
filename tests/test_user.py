from uuid import UUID

import pytest

from taskflow.exceptions import InvalidEmailError, InvalidPasswordError
from taskflow.user import User


def test_create_user() -> None:
    user = User(
        email="max@example.com",
        password_hash="hashed-password",
    )
    assert user.id is not None
    assert user.email == "max@example.com"
    assert user.password_hash == "hashed-password"


def test_normalizes_email() -> None:
    user = User(email="   MAX@EXAMPLE.COM  ", password_hash="hashed-password")
    assert user.id is not None
    assert isinstance(user.id, UUID)
    assert user.email == "max@example.com"
    assert user.password_hash == "hashed-password"


def test_rejects_empty_email() -> None:
    with pytest.raises(InvalidEmailError):
        User(email="  ", password_hash="hashed_password")


def test_rejects_empty_password_hash() -> None:
    with pytest.raises(InvalidPasswordError):
        User(email="max@example.com", password_hash="   ")
