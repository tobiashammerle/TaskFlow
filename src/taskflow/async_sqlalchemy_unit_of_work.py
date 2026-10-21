from types import TracebackType
from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from taskflow.async_sqlalchemy_task_repository import AsyncSqlAlchemyTaskRepository
from taskflow.async_sqlalchemy_user_repository import AsyncSqlalchemyUserRepository
from taskflow.database import SessionFactory


class AsyncSqlalchemyUnitOfWork:
    def __init__(
        self, session_factory: async_sessionmaker[AsyncSession] = SessionFactory
    ) -> None:
        self.session_factory = session_factory
        self.session: AsyncSession | None = None
        self._tasks: AsyncSqlAlchemyTaskRepository | None = None
        self._users: AsyncSqlalchemyUserRepository | None = None

    async def __aenter__(self) -> Self:
        self.session = self.session_factory()
        self._tasks = AsyncSqlAlchemyTaskRepository(self.session)
        self._users = AsyncSqlalchemyUserRepository(self.session)
        return self

    @property
    def tasks(self) -> AsyncSqlAlchemyTaskRepository:
        if self._tasks is None:
            raise RuntimeError("UnitOfWork wurde nicht gestartet.")
        return self._tasks

    @property
    def users(self) -> AsyncSqlalchemyUserRepository:
        if self._users is None:
            raise RuntimeError("UnitOfWork wurde nicht gestartet.")
        return self._users

    async def __aexit__(
        self,
        exc_type: type[Exception] | None,
        exc_value: Exception | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.rollback()
        if self.session is not None:
            await self.session.close()

    async def commit(self) -> None:
        if self.session is None:
            raise RuntimeError("UnitOfWork wurde nicht gestartet.")
        await self.session.commit()

    async def rollback(self) -> None:
        if self.session is None:
            raise RuntimeError("UnitOfWork wurde nicht gestartet.")
        await self.session.rollback()
