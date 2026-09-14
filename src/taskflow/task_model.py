from datetime import date
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column

from taskflow.database import Base


class TaskModel(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[UUID] = mapped_column(unique=True)
    title: Mapped[str] = mapped_column()
    completed: Mapped[bool] = mapped_column()
    priority: Mapped[str] = mapped_column()
    due_date: Mapped[date | None] = mapped_column()
