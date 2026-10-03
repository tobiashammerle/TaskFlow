import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from taskflow.database import Base
from taskflow.sqlalchemy_user_repository import SqlalchemyUserRepository
from taskflow.user import User


@pytest.fixture
def repository():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = Session(engine)
    repository = SqlalchemyUserRepository(session)
    yield repository
    session.close()


def test_add(repository: SqlalchemyUserRepository) -> None:
    user = User(email="max@example.com", password_hash="hashed-password")
    repository.add(user)
    loaded_user = repository.get_by_email(user.email)
    assert loaded_user is not None
    assert loaded_user.id == user.id
    assert loaded_user.email == user.email
    assert loaded_user.password_hash == user.password_hash


def test_get_by_email_returns_none_when_user_does_not_exist(
    repository: SqlalchemyUserRepository,
) -> None:
    loaded_user = repository.get_by_email("unknown@example.com")
    assert loaded_user is None
