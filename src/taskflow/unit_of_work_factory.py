from taskflow.database import SessionFactory
from taskflow.repository_factory import create_repository
from taskflow.repository_type import RepositoryType
from taskflow.repository_unit_of_work import RepositoryUnitOfWork
from taskflow.sqlalchemy_unit_of_work import SqlalchemyUnitOfWork
from taskflow.unit_of_work import UnitOfWork


def create_unit_of_work(repository_type: RepositoryType) -> UnitOfWork:
    if repository_type == RepositoryType.SQLALCHEMY:
        return SqlalchemyUnitOfWork(SessionFactory)
    repository = create_repository(repository_type)
    return RepositoryUnitOfWork(repository)
