from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from taskflow.database import Base
from taskflow.sqlalchemy_task_repository import SqlalchemyTaskRepository
from taskflow.sqlalchemy_unit_of_work import SqlalchemyUnitOfWork
from taskflow.task import Task

type UowSetup = tuple[SqlalchemyUnitOfWork, sessionmaker[Session]]


@pytest.fixture
def uow_setup(tmp_path: Path) -> UowSetup:
    db_path = tmp_path / "test.db"
    engine = create_engine(f"sqlite:///{db_path}")
    Base.metadata.create_all(engine)
    test_session_factory = sessionmaker(bind=engine)
    uow = SqlalchemyUnitOfWork(test_session_factory)
    return uow, test_session_factory


def test_commit_persists_task(uow_setup: UowSetup) -> None:
    uow, test_session_factory = uow_setup
    task = Task(title="Test Task")

    with uow:
        uow.tasks.add(task)
        uow.commit()

    new_session = test_session_factory()
    try:
        new_repository = SqlalchemyTaskRepository(new_session)
        loaded_task = new_repository.get_by_id(task.id)
        assert loaded_task is not None
        assert loaded_task.title == task.title
        assert loaded_task.completed == task.completed
        assert loaded_task.priority == task.priority
    finally:
        new_session.close()


def test_without_commit_task_is_not_persisted(uow_setup: UowSetup) -> None:
    uow, test_session_factory = uow_setup
    task = Task(title="Test Task")

    with uow:
        uow.tasks.add(task)
        # No commit here

    new_session = test_session_factory()
    try:
        new_repository = SqlalchemyTaskRepository(new_session)
        loaded_task = new_repository.get_by_id(task.id)
        assert loaded_task is None
    finally:
        new_session.close()


def test_exception_rolls_back_and_is_propagated(uow_setup: UowSetup) -> None:
    uow, test_session_factory = uow_setup
    task = Task(title="Test Task")
    with pytest.raises(RuntimeError):
        with uow:
            uow.tasks.add(task)
            raise RuntimeError("Boom!")

    new_session = test_session_factory()
    try:
        new_repository = SqlalchemyTaskRepository(new_session)
        loaded_task = new_repository.get_by_id(task.id)
        assert loaded_task is None
    finally:
        new_session.close()
