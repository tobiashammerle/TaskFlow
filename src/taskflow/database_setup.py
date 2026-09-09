from taskflow.database import Base, engine
from taskflow.task_model import TaskModel  # noqa: F401


def initialize_database() -> None:
    """Initialize the database and create the tasks table."""
    Base.metadata.create_all(engine)
