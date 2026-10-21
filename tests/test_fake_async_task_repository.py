from uuid import uuid4

import pytest

from taskflow.task import Task
from tests.fakes import FakeAsyncTaskRepository


@pytest.mark.asyncio
async def test_add_and_get_task():
    repository = FakeAsyncTaskRepository()
    task = Task("Testaufgabe", owner_id=uuid4())
    await repository.add(task)
    loaded_task = await repository.get_by_id(task.id)
    assert loaded_task is not None
    assert loaded_task.id == task.id
    assert loaded_task.title == task.title


@pytest.mark.asyncio
async def test_get_by_id_returns_none_for_unknown_id():
    repository = FakeAsyncTaskRepository()
    known_owner_id = uuid4()
    task = Task("Testaufgabe", known_owner_id)
    await repository.add(task)
    unknown_task_id = uuid4()
    loaded_task = await repository.get_by_id(unknown_task_id)
    assert loaded_task is None


@pytest.mark.asyncio
async def test_get_all_returns_added_tasks():
    repository = FakeAsyncTaskRepository()
    owner_id = uuid4()
    task_1 = Task("Aufgabe 1", owner_id)
    task_2 = Task("Aufgabe 2", owner_id)
    await repository.add(task_1)
    await repository.add(task_2)
    loaded_tasks = await repository.get_all()
    assert len(loaded_tasks) == 2
    assert {task.id for task in loaded_tasks} == {task_1.id, task_2.id}
    assert {task.title for task in loaded_tasks} == {task_1.title, task_2.title}


@pytest.mark.asyncio
async def test_get_all_by_owner_filter_tasks():
    repository = FakeAsyncTaskRepository()
    owner_a_id = uuid4()
    owner_b_id = uuid4()
    task_1 = Task("Aufgabe 1", owner_a_id)
    task_2 = Task("Aufgabe 2", owner_b_id)
    task_3 = Task("Aufgabe 3", owner_a_id)
    await repository.add(task_1)
    await repository.add(task_2)
    await repository.add(task_3)
    loaded_tasks = await repository.get_all_by_owner(owner_a_id)
    assert len(loaded_tasks) == 2
    assert {task.id for task in loaded_tasks} == {task_1.id, task_3.id}
    assert {task.title for task in loaded_tasks} == {task_1.title, task_3.title}


@pytest.mark.asyncio
async def test_update_changes_task():
    repository = FakeAsyncTaskRepository()
    owner_id = uuid4()
    task = Task("Alte Aufgabe", owner_id)
    task_id = task.id
    await repository.add(task)
    updated_task = Task("Neue Aufgabe", owner_id, task_id=task_id)
    await repository.update(updated_task)
    loaded_task = await repository.get_by_id(task_id)
    assert loaded_task is not None
    assert loaded_task.id == task_id
    assert loaded_task.title == "Neue Aufgabe"


@pytest.mark.asyncio
async def test_delete_removes_task():
    repository = FakeAsyncTaskRepository()
    owner = uuid4()
    task_1 = Task("Aufgabe 1", owner_id=owner)
    task_2 = Task("Aufgabe 2", owner_id=owner)
    await repository.add(task_1)
    await repository.add(task_2)
    await repository.delete(task_1.id)
    assert await repository.get_by_id(task_1.id) is None
    loaded_tasks = await repository.get_all()
    assert len(loaded_tasks) == 1
    assert loaded_tasks[0].title == "Aufgabe 2"
    assert loaded_tasks[0].id == task_2.id


@pytest.mark.asyncio
async def test_save_replaces_tasks():
    repository = FakeAsyncTaskRepository()
    owner = uuid4()
    task_1 = Task("Aufgabe 1", owner)
    task_2 = Task("Aufgabe 2", owner)
    await repository.add(task_1)
    await repository.save([task_2])
    loaded_tasks = await repository.get_all()
    assert len(loaded_tasks) == 1
    assert loaded_tasks[0].id == task_2.id
    assert loaded_tasks[0].title == task_2.title
