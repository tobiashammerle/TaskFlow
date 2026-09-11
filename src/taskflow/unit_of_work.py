from types import TracebackType
from typing import Protocol, Self

from taskflow.task_repository import TaskRepository


class UnitOfWork(Protocol):
    @property
    def tasks(self) -> TaskRepository: ...

    def __enter__(self) -> Self: ...

    def __exit__(
        self,
        exc_type: type[Exception] | None,
        exc_value: Exception | None,
        traceback: TracebackType | None,
    ) -> None: ...

    def commit(self) -> None: ...

    def rollback(self) -> None: ...
