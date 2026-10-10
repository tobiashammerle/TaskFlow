from datetime import date
from uuid import UUID, uuid4

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from taskflow.database import Base
from taskflow.exceptions import TaskNotFoundError
from taskflow.priority import Priority
from taskflow.sqlalchemy_task_repository import SqlalchemyTaskRepository
from taskflow.task import Task
from taskflow.user_model import UserModel  # noqa: F401


@pytest.fixture
def repository():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = Session(engine)
    repository = SqlalchemyTaskRepository(session)
    yield repository
    session.close()


@pytest.fixture
def owner_id():
    return uuid4()


def test_add(repository: SqlalchemyTaskRepository, owner_id: UUID) -> None:
    task = Task(title="SQLAlchemy testen", owner_id=owner_id)
    repository.add(task)
    loaded_task = repository.get_by_id(task.id)
    assert loaded_task is not None
    assert loaded_task.title == "SQLAlchemy testen"
    assert loaded_task.id == task.id


def test_get_all(repository: SqlalchemyTaskRepository, owner_id: UUID) -> None:
    task1 = Task(title="Task 1", owner_id=owner_id)
    task2 = Task(title="Task 2", owner_id=owner_id)
    repository.add(task1)
    repository.add(task2)
    tasks = repository.get_all()
    assert len(tasks) == 2
    assert any(t.title == "Task 1" for t in tasks)
    assert any(t.title == "Task 2" for t in tasks)


def test_update(repository: SqlalchemyTaskRepository, owner_id: UUID) -> None:
    task = Task(title="Ursprünglicher Titel", owner_id=owner_id)
    repository.add(task)
    task.complete()
    task.title = "Aktualisierter Titel"
    repository.update(task)
    updated_task = repository.get_by_id(task.id)
    assert updated_task is not None
    assert updated_task.title == "Aktualisierter Titel"
    assert updated_task.completed is True


def test_delete(repository: SqlalchemyTaskRepository, owner_id: UUID) -> None:
    task = Task(title="Zu löschender Task", owner_id=owner_id)
    repository.add(task)
    assert repository.get_by_id(task.id) is not None
    repository.delete(task.id)
    deleted_task = repository.get_by_id(task.id)
    assert deleted_task is None


def test_save(repository: SqlalchemyTaskRepository, owner_id: UUID) -> None:
    task1 = Task(title="A", owner_id=owner_id)
    task2 = Task(title="B", owner_id=owner_id)
    task3 = Task(title="C", owner_id=owner_id)
    repository.save([task1, task2, task3])
    task4 = Task(title="X", owner_id=owner_id)
    task5 = Task(title="Y", owner_id=owner_id)
    repository.save([task4, task5])
    tasks = repository.get_all()
    assert len(tasks) == 2
    assert any(t.title == "X" for t in tasks)
    assert any(t.title == "Y" for t in tasks)


def test_update_raises_error_when_task_not_found(
    repository: SqlalchemyTaskRepository,
    owner_id: UUID,
) -> None:
    task = Task(title="Nicht existierender Task", owner_id=owner_id)
    with pytest.raises(TaskNotFoundError):
        repository.update(task)


def test_delete_raises_error_when_task_not_found(
    repository: SqlalchemyTaskRepository,
) -> None:
    unknown_task_id = uuid4()
    with pytest.raises(TaskNotFoundError):
        repository.delete(unknown_task_id)


def test_get_by_id_restores_all_task_fields(
    repository: SqlalchemyTaskRepository,
    owner_id: UUID,
) -> None:
    task = Task(
        title="Test Task",
        priority=Priority.HIGH,
        due_date=date(2026, 9, 15),
        owner_id=owner_id,
    )
    task.complete()
    repository.add(task)
    loaded_task = repository.get_by_id(task.id)
    assert loaded_task is not None
    assert loaded_task.id == task.id
    assert loaded_task.title == task.title
    assert loaded_task.completed == task.completed
    assert loaded_task.priority == task.priority
    assert loaded_task.due_date == task.due_date


def test_get_all_by_owner_returns_only_tasks_of_owner(
    repository: SqlalchemyTaskRepository,
) -> None:
    owner_a_id = uuid4()
    owner_b_id = uuid4()
    task_1 = Task(title="Task 1", owner_id=owner_a_id)
    task_2 = Task(title="Task 2", owner_id=owner_a_id)
    task_3 = Task(title="Task 3", owner_id=owner_b_id)
    repository.add(task_1)
    repository.add(task_2)
    repository.add(task_3)
    tasks = repository.get_all_by_owner(owner_a_id)
    assert len(tasks) == 2
    assert all(task.owner_id == owner_a_id for task in tasks)
