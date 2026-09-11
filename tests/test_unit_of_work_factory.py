from taskflow.repository_type import RepositoryType
from taskflow.repository_unit_of_work import RepositoryUnitOfWork
from taskflow.sqlalchemy_unit_of_work import SqlalchemyUnitOfWork
from taskflow.unit_of_work_factory import create_unit_of_work


def test_create_unit_of_work_returns_sqlalchemy_unit_of_work() -> None:
    uow = create_unit_of_work(repository_type=RepositoryType.SQLALCHEMY)
    assert isinstance(uow, SqlalchemyUnitOfWork)


def test_create_unit_of_work_returns_repository_unit_of_work_for_json() -> None:
    uow = create_unit_of_work(repository_type=RepositoryType.JSON)
    assert isinstance(uow, RepositoryUnitOfWork)


def test_create_unit_of_work_returns_repository_unit_of_work_for_sqlite() -> None:
    uow = create_unit_of_work(repository_type=RepositoryType.SQLITE)
    assert isinstance(uow, RepositoryUnitOfWork)
