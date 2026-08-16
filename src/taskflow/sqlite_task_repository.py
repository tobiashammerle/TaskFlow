import sqlite3
from datetime import date
from pathlib import Path
from uuid import UUID

from taskflow.priority import Priority
from taskflow.task import Task


class SqliteTaskRepository:
    """Speichert Aufgaben in einer SQLite-Datenbank."""

    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path

    def initialize_database(self) -> None:
        connection = sqlite3.connect(self.database_path)
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS
            tasks (
                    id INTEGER PRIMARY KEY
                AUTOINCREMENT,
                task_id TEXT NOT NULL UNIQUE,
                title TEXT NOT NULL,
                completed INTEGER NOT NULL,
                priority TEXT NOT NULL,
                due_date TEXT
            )
            """
        )
        connection.commit()
        connection.close()

    def save(self, tasks: list[Task]) -> None:
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                DELETE FROM tasks
                """
            )
            for task in tasks:
                cursor.execute(
                    """
                    INSERT INTO tasks (
                    task_id,
                    title,
                    completed,
                    priority,
                    due_date
                    )
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        str(task.id),
                        task.title,
                        int(task.completed),
                        task.priority.value,
                        (
                            task.due_date.isoformat()
                            if task.due_date is not None
                            else None
                        ),
                    ),
                )

    def get_all(self) -> list[Task]:
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT task_id, title, completed, priority, due_date
                FROM tasks
                ORDER BY id
                """
            )
            rows = cursor.fetchall()
        tasks: list[Task] = []

        for task_id, title, completed, priority, due_date_value in rows:
            task = Task(
                title=title,
                priority=Priority(priority),
                due_date=(
                    date.fromisoformat(due_date_value)
                    if due_date_value is not None
                    else None
                ),
                task_id=UUID(task_id),
            )
            if bool(completed):
                task.complete()
            tasks.append(task)
        return tasks

    def get_by_id(self, task_id: UUID) -> Task | None:
        """Lädt eine Aufgabe anhand ihrer ID aus der SQLite-Datenbank."""
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT task_id, title, completed, priority, due_date
                FROM tasks
                WHERE task_id = ?
                """,
                (str(task_id),),
            )
            row = cursor.fetchone()

        if row is None:
            return None

        task_id, title, completed, priority, due_date_value = row
        task = Task(
            title=title,
            priority=Priority(priority),
            due_date=(
                date.fromisoformat(due_date_value)
                if due_date_value is not None
                else None
            ),
            task_id=UUID(task_id),
        )
        if bool(completed):
            task.complete()
        return task

    def add(self, task: Task) -> None:
        """Fügt eine Aufgabe in die SQLite-Datenbank ein."""
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO tasks (
                    task_id,
                    title,
                    completed,
                    priority,
                    due_date
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    str(task.id),
                    task.title,
                    int(task.completed),
                    task.priority.value,
                    (task.due_date.isoformat() if task.due_date is not None else None),
                ),
            )

    def update(self, task: Task) -> None:
        """Aktualisiert eine Aufgabe in der SQLite-Datenbank."""
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                UPDATE tasks
                SET title = ?,
                    completed = ?,
                    priority = ?,
                    due_date = ?
                WHERE task_id = ?
                """,
                (
                    task.title,
                    int(task.completed),
                    task.priority.value,
                    (task.due_date.isoformat() if task.due_date is not None else None),
                    str(task.id),
                ),
            )

    def delete(self, task_id: UUID) -> None:
        """Löscht eine Aufgabe anhand ihrer ID aus der SQLite-Datenbank."""
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                DELETE FROM tasks
                WHERE task_id = ?
                """,
                (str(task_id),),
            )
