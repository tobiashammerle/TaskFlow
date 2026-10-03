from types import TracebackType
from typing import Protocol, Self

from taskflow.user_repository import UserRepository


class UserUnitOfWork(Protocol):
    @property
    def users(self) -> UserRepository: ...

    def __enter__(self) -> Self: ...

    def __exit__(
        self,
        exc_type: type[Exception] | None,
        exc_value: Exception | None,
        traceback: TracebackType | None,
    ) -> None: ...

    def commit(self) -> None: ...
