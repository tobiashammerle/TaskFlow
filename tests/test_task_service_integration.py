from pathlib import Path

from taskflow.sqlite_task_repository import SqliteTaskRepository
from taskflow.task_service import TaskService
from tests.fakes import FakeTaskRepository


def test_add_task_saves_task_in_repository():
    repository = FakeTaskRepository() # erstelle Repository (siehe settings.ini)
    task_service = TaskService(repository) # einen echten TaskService erstellen
    anzahl_tests_vorher = len(task_service.get_tasks())
    task_service.add_task("Englisch lernen")
    
    assert len(task_service.get_tasks()) == anzahl_tests_vorher +1
    assert task_service.get_tasks()[-1].title == "Englisch lernen"

def test_add_task_persists_in_sqlite(tmp_path: Path):
    database_path = tmp_path /"test_tasks.db"
    repository = SqliteTaskRepository(database_path)
    repository.initialize_database()
    task_service = TaskService(repository)
    task_service.add_task("Python lernen")
    assert len(task_service.get_tasks()) == 1
    assert task_service.get_tasks()[0].title == "Python lernen"

def test_task_survives_new_service_instance(tmp_path: Path) -> None:
    database_path = tmp_path /"test_tasks.db"
    repository_1 = SqliteTaskRepository(database_path)
    repository_1.initialize_database()
    task_service_1 = TaskService(repository_1)
    task_service_1.add_task("Python lernen")
    

    repository_2 = SqliteTaskRepository(database_path)
    repository_2.initialize_database()
    task_service_2 = TaskService(repository_2)
    assert len(task_service_2.get_tasks()) == 1
    assert task_service_2.get_tasks()[0].title == "Python lernen"


def test_completed_task_state_persists_in_sqlite(tmp_path: Path) -> None:
    database_path = tmp_path /"test_tasks.db"
    repository_1 = SqliteTaskRepository(database_path)
    repository_1.initialize_database()
    task_service_1 = TaskService(repository_1)
    task_service_1.add_task("Python lernen")
    task_service_1.complete_task(0)

    repository_2 = SqliteTaskRepository(database_path)
    repository_2.initialize_database()
    task_service_2 = TaskService(repository_2)
    assert len(task_service_2.get_tasks()) == 1
    assert task_service_2.get_tasks()[0].title == "Python lernen"
    assert task_service_2.get_tasks()[0].completed is True


def test_removed_task_does_not_appear_after_new_service_instance(tmp_path: Path) -> None:
    database_path = tmp_path /"test_tasks.db"
    repository_1 = SqliteTaskRepository(database_path)
    repository_1.initialize_database()
    task_service_1 = TaskService(repository_1)
    task_service_1.add_task("Python lernen")
    task_service_1.remove_task(0)
    repository_2 = SqliteTaskRepository(database_path)
    repository_2.initialize_database()
    task_service_2 = TaskService(repository_2)
    assert len(task_service_2.get_tasks()) == 0






    



    