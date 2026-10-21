from uuid import uuid4

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from taskflow.async_sqlalchemy_task_repository import (
    AsyncSqlAlchemyTaskRepository,
)
from taskflow.database import Base
from taskflow.task import Task

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
# engine = create_async_engine(TEST_DATABASE_URL, echo=False)


@pytest_asyncio.fixture
async def test_session():
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
    )
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    session_factory = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
    )
    async with session_factory() as session:
        yield session

    await engine.dispose()


@pytest.mark.asyncio
async def test_async_repository_add_and_get(test_session: AsyncSession):
    repository = AsyncSqlAlchemyTaskRepository(test_session)
    owner_id = uuid4()
    task = Task(title="Async Datenbanktest", owner_id=owner_id)
    await repository.add(task)
    await test_session.commit()
    loaded_task = await repository.get_by_id(task.id)
    assert loaded_task is not None
    assert loaded_task.title == "Async Datenbanktest"
    assert loaded_task.id == task.id


@pytest.mark.asyncio
async def test_async_repository_update_changes_task(
    test_session: AsyncSession,
):
    repository = AsyncSqlAlchemyTaskRepository(test_session)
    owner_id = uuid4()
    task = Task(title="Alte Aufgabe", owner_id=owner_id)
    task_id = task.id
    await repository.add(task)
    await test_session.commit()
    updated_task = Task("Neue Aufgabe", owner_id, task_id=task_id)
    await repository.update(updated_task)
    await test_session.commit()
    loaded_task = await repository.get_by_id(task_id)
    assert loaded_task is not None
    assert loaded_task.id == task_id
    assert loaded_task.title == "Neue Aufgabe"


@pytest.mark.asyncio
async def test_async_repository_delete_removes_task(
    test_session: AsyncSession,
):
    repository = AsyncSqlAlchemyTaskRepository(test_session)
    owner = uuid4()
    task_1 = Task("Aufgabe 1", owner_id=owner)
    task_2 = Task("Aufgabe 2", owner_id=owner)
    await repository.add(task_1)
    await repository.add(task_2)
    await test_session.commit()
    await repository.delete(task_1.id)
    await test_session.commit()
    assert await repository.get_by_id(task_1.id) is None
    loaded_tasks = await repository.get_all()
    assert len(loaded_tasks) == 1
    assert loaded_tasks[0].title == "Aufgabe 2"
    assert loaded_tasks[0].id == task_2.id


@pytest.mark.asyncio
async def test_get_all_by_owner_filter_tasks(
    test_session: AsyncSession,
):
    repository = AsyncSqlAlchemyTaskRepository(test_session)
    owner_a_id = uuid4()
    owner_b_id = uuid4()
    task_1 = Task("Aufgabe 1", owner_a_id)
    task_2 = Task("Aufgabe 2", owner_b_id)
    task_3 = Task("Aufgabe 3", owner_a_id)
    await repository.add(task_1)
    await repository.add(task_2)
    await repository.add(task_3)
    await test_session.commit()
    loaded_tasks = await repository.get_all_by_owner(owner_a_id)
    assert len(loaded_tasks) == 2
    assert {task.id for task in loaded_tasks} == {task_1.id, task_3.id}
    assert {task.title for task in loaded_tasks} == {task_1.title, task_3.title}
