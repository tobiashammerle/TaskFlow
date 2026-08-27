from taskflow import repository_factory
from taskflow.json_task_repository import JsonTaskRepository
from taskflow.repository_type import RepositoryType
from taskflow.sqlite_task_repository import SqliteTaskRepository


def test_create_repository_returns_sqlite_repository() -> None:
    repository = repository_factory.create_repository(RepositoryType.SQLITE)
    assert isinstance(repository, SqliteTaskRepository)


def test_create_repository_returns_json_repository() -> None:
    repository = repository_factory.create_repository(RepositoryType.JSON)
    assert isinstance(repository, JsonTaskRepository)
