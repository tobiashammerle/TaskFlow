from taskflow.database_setup import initialize_database
from taskflow.repository_type import RepositoryType


def initialize_application(repository_type: RepositoryType) -> None:
    if repository_type == RepositoryType.SQLALCHEMY:
        initialize_database()
