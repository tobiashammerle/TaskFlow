from types import TracebackType
from typing import Protocol, Self

from taskflow.async_user_repository import AsyncUserRepository


class AsyncUserUnitOfWork(Protocol):
    @property
    def users(self) -> AsyncUserRepository: ...

    async def __aenter__(self) -> Self: ...

    async def __aexit__(
        self,
        exc_type: type[Exception] | None,
        exc_value: Exception | None,
        traceback: TracebackType | None,
    ) -> None: ...

    async def commit(self) -> None: ...
