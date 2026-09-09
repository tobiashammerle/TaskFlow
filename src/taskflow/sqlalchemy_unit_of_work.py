from types import TracebackType
from typing import Self

from sqlalchemy.orm import Session, sessionmaker

from taskflow.database import SessionFactory
from taskflow.sqlalchemy_task_repository import SqlalchemyTaskRepository


class SqlalchemyUnitOfWork:
    def __init__(self, session_factory: sessionmaker[Session] = SessionFactory) -> None:
        self.session_factory = session_factory
        self.session: Session | None = None
        self._tasks: SqlalchemyTaskRepository | None = None

    def __enter__(self) -> Self:
        self.session = self.session_factory()
        self._tasks = SqlalchemyTaskRepository(self.session)
        return self

    @property
    def tasks(self) -> SqlalchemyTaskRepository:
        if self._tasks is None:
            raise RuntimeError("UnitOfWork wurde nicht gestartet.")
        return self._tasks

    def __exit__(
        self,
        exc_type: type[Exception] | None,
        exc_value: Exception | None,
        traceback: TracebackType | None,
    ) -> None:
        self.rollback()
        if self.session is not None:
            self.session.close()

    def commit(self) -> None:
        if self.session is None:
            raise RuntimeError("UnitOfWork wurde nicht gestartet.")
        self.session.commit()

    def rollback(self) -> None:
        if self.session is None:
            raise RuntimeError("UnitOfWork wurde nicht gestartet.")
        self.session.rollback()
