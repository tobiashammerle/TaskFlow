import pytest

from taskflow.application.register_user import RegisterUser
from taskflow.exceptions import DuplicateUserError
from tests.fakes import FakePasswordHasher, FakeUserUnitOfWork


def test_register_user_with_hashed_password() -> None:
    unit_of_work = FakeUserUnitOfWork()
    password_hasher = FakePasswordHasher()
    register_user = RegisterUser(
        unit_of_work=unit_of_work, password_hasher=password_hasher
    )

    register_user.execute(email="max@example.com", password="TestPassword123")

    user = unit_of_work.users.get_by_email("max@example.com")
    assert user is not None
    assert unit_of_work.committed is True
    assert user.password_hash == "hashed-TestPassword123"


def test_raises_Duplicate_User_Error_when_user_already_exists() -> None:
    unit_of_work = FakeUserUnitOfWork()
    password_hasher = FakePasswordHasher()
    register_user = RegisterUser(
        unit_of_work=unit_of_work, password_hasher=password_hasher
    )
    register_user.execute(email="max@example.com", password="TestPassword123")
    with pytest.raises(DuplicateUserError):
        register_user.execute(email="max@example.com", password="TestPassword123")


def test_rejects_duplicate_user_with_unnormalized_email() -> None:
    unit_of_work = FakeUserUnitOfWork()
    password_hasher = FakePasswordHasher()
    register_user = RegisterUser(
        unit_of_work=unit_of_work, password_hasher=password_hasher
    )
    register_user.execute(email="max@example.com", password="TestPassword123")
    with pytest.raises(DuplicateUserError):
        register_user.execute(email="MAX@EXAMPLE.COM", password="TestPassword123")
