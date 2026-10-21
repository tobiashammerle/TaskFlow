from types import TracebackType
from typing import Protocol, Self

from taskflow.async_task_repository import AsyncTaskRepository


class AsyncUnitOfWork(Protocol):
    @property
    def tasks(self) -> AsyncTaskRepository: ...

    async def __aenter__(self) -> Self: ...

    async def __aexit__(
        self,
        exc_type: type[Exception] | None,
        exc_value: Exception | None,
        traceback: TracebackType | None,
    ) -> None: ...

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...
