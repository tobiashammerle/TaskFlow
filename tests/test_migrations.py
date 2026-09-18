from pathlib import Path

from alembic.config import Config
from sqlalchemy import create_engine, inspect

from alembic import command


def test_upgrade_head_creates_current_schema(tmp_path: Path) -> None:
    database = tmp_path / "migration_test.db"
    database_url = f"sqlite:///{database}"
    alembic_config = Config("alembic.ini")
    alembic_config.set_main_option("sqlalchemy.url", database_url)
    command.upgrade(alembic_config, "head")
    engine = create_engine(database_url)
    inspector = inspect(engine)
    assert "tasks" in inspector.get_table_names()
    columns = {column["name"] for column in inspector.get_columns("tasks")}
    assert "description" in columns
