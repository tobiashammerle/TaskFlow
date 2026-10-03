import pytest

from taskflow.application.authenticate_user import AuthenticateUser
from taskflow.application.login_user import LoginUser
from taskflow.exceptions import InvalidCredentialsError
from taskflow.user import User
from tests.fakes import (
    FakePasswordHasher,
    FakeTokenService,
    FakeUserUnitOfWork,
)


def test_returns_access_token_when_credentials_are_valid() -> None:
    unit_of_work = FakeUserUnitOfWork()
    password_hasher = FakePasswordHasher()
    token_service = FakeTokenService()
    user = User(
        email="max@example.com",
        password_hash="hashed-TestPassword123",
    )
    unit_of_work.users.add(user)
    authenticate_user = AuthenticateUser(
        unit_of_work=unit_of_work,
        password_hasher=password_hasher,
    )
    login_user = LoginUser(
        authenticate_user=authenticate_user,
        token_service=token_service,
    )
    token = login_user.execute(
        email="max@example.com",
        password="TestPassword123",
    )
    assert token == f"token-{user.id}"


def test_raises_invalid_credentials_when_password_is_wrong() -> None:
    unit_of_work = FakeUserUnitOfWork()
    password_hasher = FakePasswordHasher()
    token_service = FakeTokenService()
    user = User(
        email="max@example.com",
        password_hash="hashed-TestPassword123",
    )
    unit_of_work.users.add(user)
    authenticate_user = AuthenticateUser(
        unit_of_work=unit_of_work,
        password_hasher=password_hasher,
    )
    login_user = LoginUser(
        authenticate_user=authenticate_user,
        token_service=token_service,
    )
    with pytest.raises(InvalidCredentialsError):
        login_user.execute(email="max@example.com", password="FalschesPasswort")
