from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from taskflow.exceptions import TaskNotFoundError
from taskflow.priority import Priority
from taskflow.task import Task
from taskflow.task_model import TaskModel
from taskflow.task_repository import TaskRepository


class SqlalchemyTaskRepository(TaskRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, task: Task) -> None:
        task_model = self._to_model(task)
        self.session.add(task_model)

    def _to_domain(self, task_model: TaskModel) -> Task:
        priority = Priority(task_model.priority)
        return Task(
            task_id=task_model.task_id,
            title=task_model.title,
            completed=task_model.completed,
            priority=priority,
            due_date=task_model.due_date,
        )

    def _to_model(self, task: Task) -> TaskModel:
        priority = task.priority.value
        task_model = TaskModel(
            task_id=task.id,
            title=task.title,
            completed=task.completed,
            priority=priority,
            due_date=task.due_date,
        )
        return task_model

    def get_all(self) -> list[Task]:
        statement = select(TaskModel)
        result = self.session.execute(statement)
        task_models = result.scalars().all()
        return [self._to_domain(task_model) for task_model in task_models]

    def get_by_id(self, task_id: UUID) -> Task | None:
        statement = select(TaskModel).where(TaskModel.task_id == task_id)
        result = self.session.execute(statement)
        task_model = result.scalar_one_or_none()
        if task_model is not None:
            return self._to_domain(task_model)
        return None

    def update(self, task: Task) -> None:
        statement = select(TaskModel).where(TaskModel.task_id == task.id)
        result = self.session.execute(statement)
        task_model = result.scalar_one_or_none()
        if task_model is None:
            raise TaskNotFoundError(f"Task mit ID {task.id} nicht gefunden.")
        task_model.title = task.title
        task_model.completed = task.completed
        task_model.priority = task.priority.value
        task_model.due_date = task.due_date

    def delete(self, task_id: UUID) -> None:
        statement = select(TaskModel).where(TaskModel.task_id == task_id)
        result = self.session.execute(statement)
        task_model = result.scalar_one_or_none()
        if task_model is None:
            raise TaskNotFoundError(f"Task mit ID {task_id} nicht gefunden.")
        self.session.delete(task_model)

    def save(self, tasks: list[Task]) -> None:
        statement = delete(TaskModel)
        self.session.execute(statement)
        for task in tasks:
            self.add(task)
