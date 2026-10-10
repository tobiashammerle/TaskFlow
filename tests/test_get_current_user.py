from uuid import uuid4

import pytest

from taskflow.application.get_current_user import GetCurrentUser
from taskflow.exceptions import InvalidTokenError
from taskflow.user import User
from tests.fakes import FakeTokenService, FakeUserUnitOfWork


def test_get_current_user_returns_user_for_valid_token() -> None:
    user = User(email="max@example.com", password_hash="hashed-password")
    unit_of_work = FakeUserUnitOfWork()
    unit_of_work.users.add(user)
    token_service = FakeTokenService()
    token = token_service.create_access_token(user.id)
    use_case = GetCurrentUser(unit_of_work, token_service)
    current_user = use_case.execute(token)
    assert current_user == user


def test_get_current_user_raises_error_when_user_does_not_exist() -> None:
    unit_of_work = FakeUserUnitOfWork()
    token_service = FakeTokenService()
    user_id = uuid4()
    token = token_service.create_access_token(user_id)
    use_case = GetCurrentUser(unit_of_work, token_service)
    with pytest.raises(InvalidTokenError):
        use_case.execute(token)
