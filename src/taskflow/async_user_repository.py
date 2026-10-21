from typing import Protocol
from uuid import UUID

from taskflow.user import User


class AsyncUserRepository(Protocol):
    async def add(self, user: User) -> None: ...

    async def get_by_email(self, email: str) -> User | None: ...

    async def get_by_id(self, user_id: UUID) -> User | None: ...
