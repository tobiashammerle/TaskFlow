import pytest
from taskflow.repository_type import RepositoryType
from taskflow.exceptions import ConfigurationError
from taskflow import repository_factory
from taskflow.repository_factory import create_repository
from taskflow.sqlite_task_repository import SqliteTaskRepository
from taskflow.json_task_repository import JsonTaskRepository

def test_create_repository_returns_sqlite_repository(
        monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        repository_factory,
        "REPOSITORY",
        RepositoryType.SQLITE
    )
    repository = repository_factory.create_repository()
    assert isinstance(repository, SqliteTaskRepository)

def test_create_repository_returns_json_repository(
        monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        repository_factory,
        "REPOSITORY",
        RepositoryType.JSON
    )
    repository = repository_factory.create_repository()
    assert isinstance(repository, JsonTaskRepository)

def test_create_repository_raises_configuration_error_for_unknown_repository(
        monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        repository_factory,
        "REPOSITORY",
        "abc"
    )
    with pytest.raises(ConfigurationError):
        repository_factory.create_repository()
