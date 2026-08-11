from taskflow.task_service import TaskService
from tests.fakes import FakeTaskRepository
from taskflow.sqlite_task_repository import SqliteTaskRepository
from pathlib import Path

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


    



    