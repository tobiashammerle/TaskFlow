from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from taskflow.application.create_task import CreateTask
from taskflow.application.get_tasks import GetTasks
from taskflow.database import Base
from taskflow.sqlalchemy_unit_of_work import SqlalchemyUnitOfWork
from taskflow.task_model import TaskModel  # noqa: F401


def test_application_persists_task_with_sqlalchemy(tmp_path: Path) -> None:
    database = tmp_path / "test.db"
    engine = create_engine(f"sqlite:///{database}")
    session_factory = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    write_uow = SqlalchemyUnitOfWork(session_factory)
    read_uow = SqlalchemyUnitOfWork(session_factory)
    create_task = CreateTask(write_uow)
    create_task.execute("Python lernen")
    get_tasks = GetTasks(read_uow)
    tasks = get_tasks.execute()

    assert len(tasks) == 1
    assert tasks[0].title == "Python lernen"
