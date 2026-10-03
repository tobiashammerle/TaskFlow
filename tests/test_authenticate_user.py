import pytest

from taskflow.application.authenticate_user import AuthenticateUser
from taskflow.exceptions import InvalidCredentialsError
from taskflow.user import User
from tests.fakes import FakePasswordHasher, FakeUserUnitOfWork


def test_returns_user_when_credentials_are_valid() -> None:
    unit_of_work = FakeUserUnitOfWork()
    password_hasher = FakePasswordHasher()
    user = User(
        email="max@example.com",
        password_hash="hashed-TestPassword123",
    )
    unit_of_work.users.add(user)
    authenticate_user = AuthenticateUser(
        unit_of_work=unit_of_work,
        password_hasher=password_hasher,
    )
    authenticated_user = authenticate_user.execute(
        email="max@example.com",
        password="TestPassword123",
    )
    assert authenticated_user is user


def test_raises_invalid_credentials_when_user_does_not_exist() -> None:
    unit_of_work = FakeUserUnitOfWork()
    password_hasher = FakePasswordHasher()
    authenticate_user = AuthenticateUser(
        unit_of_work=unit_of_work, password_hasher=password_hasher
    )
    with pytest.raises(InvalidCredentialsError):
        authenticate_user.execute(email="max@example.com", password="TestPassword123")


def test_raises_invalid_credentials_when_password_is_wrong() -> None:
    unit_of_work = FakeUserUnitOfWork()
    password_hasher = FakePasswordHasher()
    user = User(email="max@example.com", password_hash="hashed-TestPassword123")
    unit_of_work.users.add(user)
    authenticate_user = AuthenticateUser(
        unit_of_work=unit_of_work, password_hasher=password_hasher
    )
    with pytest.raises(InvalidCredentialsError):
        authenticate_user.execute(email="max@example.com", password="FalschesPasswort")


def test_authenticates_user_with_unnormalized_email() -> None:
    unit_of_work = FakeUserUnitOfWork()
    password_hasher = FakePasswordHasher()
    user = User(email="max@example.com", password_hash="hashed-TestPassword123")
    unit_of_work.users.add(user)
    authenticate_user = AuthenticateUser(
        unit_of_work=unit_of_work, password_hasher=password_hasher
    )
    authenticated_user = authenticate_user.execute(
        email="  MAX@EXAMPLE.COM  ",
        password="TestPassword123",
    )
    assert authenticated_user is user
