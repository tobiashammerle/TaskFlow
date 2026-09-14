from taskflow.task_repository import TaskRepository


class RepositoryUnitOfWork:
    def __init__(self, repository: TaskRepository) -> None:
        self.tasks = repository

    def __enter__(self) -> "RepositoryUnitOfWork":
        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ) -> None:
        self.rollback()

    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass
