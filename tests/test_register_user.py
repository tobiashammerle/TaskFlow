import pytest

from taskflow.application.register_user import RegisterUser
from taskflow.exceptions import DuplicateUserError
from tests.fakes import FakePasswordHasher, FakeUserRepository


def test_register_user_with_hashed_password() -> None:
    repository = FakeUserRepository()
    password_hasher = FakePasswordHasher()
    register_user = RegisterUser(repository=repository, password_hasher=password_hasher)

    register_user.execute(email="max@example.com", password="TestPassword123")

    user = repository.get_by_email("max@example.com")
    assert user is not None
    assert user.password_hash == "hashed-TestPassword123"


def test_raises_Duplicate_User_Error_when_user_already_exists() -> None:
    repository = FakeUserRepository()
    password_hasher = FakePasswordHasher()
    register_user = RegisterUser(repository=repository, password_hasher=password_hasher)
    register_user.execute(email="max@example.com", password="TestPassword123")
    with pytest.raises(DuplicateUserError):
        register_user.execute(email="max@example.com", password="TestPassword123")


def test_rejects_duplicate_user_with_unnormalized_email() -> None:
    repository = FakeUserRepository()
    password_hasher = FakePasswordHasher()
    register_user = RegisterUser(repository=repository, password_hasher=password_hasher)
    register_user.execute(email="max@example.com", password="TestPassword123")
    with pytest.raises(DuplicateUserError):
        register_user.execute(email="MAX@EXAMPLE.COM", password="TestPassword123")
