from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from taskflow.async_task_repository import AsyncTaskRepository
from taskflow.exceptions import TaskNotFoundError
from taskflow.priority import Priority
from taskflow.task import Task
from taskflow.task_model import TaskModel


class AsyncSqlAlchemyTaskRepository(AsyncTaskRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, task: Task) -> None:
        task_model = self._to_model(task)
        self.session.add(task_model)

    def _to_domain(self, task_model: TaskModel) -> Task:
        priority = Priority(task_model.priority)
        return Task(
            task_id=task_model.task_id,
            owner_id=task_model.owner_id,
            title=task_model.title,
            completed=task_model.completed,
            priority=priority,
            due_date=task_model.due_date,
        )

    def _to_model(self, task: Task) -> TaskModel:
        priority = task.priority.value
        task_model = TaskModel(
            task_id=task.id,
            owner_id=task.owner_id,
            title=task.title,
            completed=task.completed,
            priority=priority,
            due_date=task.due_date,
        )
        return task_model

    async def get_all(self) -> list[Task]:
        statement = select(TaskModel)
        result = await self.session.execute(statement)
        task_models = result.scalars().all()
        return [self._to_domain(task_model) for task_model in task_models]

    async def get_all_by_owner(self, owner_id: UUID) -> list[Task]:
        statement = select(TaskModel).where(TaskModel.owner_id == owner_id)
        result = await self.session.execute(statement)
        task_models = result.scalars().all()
        return [self._to_domain(task_model) for task_model in task_models]

    async def get_by_id(self, task_id: UUID) -> Task | None:
        statement = select(TaskModel).where(TaskModel.task_id == task_id)
        result = await self.session.execute(statement)
        task_model = result.scalar_one_or_none()
        if task_model is not None:
            return self._to_domain(task_model)
        return None

    async def update(self, task: Task) -> None:
        statement = select(TaskModel).where(TaskModel.task_id == task.id)
        result = await self.session.execute(statement)
        task_model = result.scalar_one_or_none()
        if task_model is None:
            raise TaskNotFoundError(f"Task mit ID {task.id} nicht gefunden.")
        task_model.title = task.title
        task_model.completed = task.completed
        task_model.priority = task.priority.value
        task_model.due_date = task.due_date

    async def delete(self, task_id: UUID) -> None:
        statement = select(TaskModel).where(TaskModel.task_id == task_id)
        result = await self.session.execute(statement)
        task_model = result.scalar_one_or_none()
        if task_model is None:
            raise TaskNotFoundError(f"Task mit ID {task_id} nicht gefunden.")
        await self.session.delete(task_model)

    async def save(self, tasks: list[Task]) -> None:
        statement = delete(TaskModel)
        await self.session.execute(statement)
        for task in tasks:
            await self.add(task)
