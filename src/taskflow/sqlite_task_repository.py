import sqlite3
from datetime import date
from pathlib import Path
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
                    title,
                    completed,
                    priority,
                    due_date
                    )
                    VALUES (?, ?, ?, ?)
                    """,
                (
                    task.title,
                    int(task.completed),
                    task.priority.value,
                    (task.due_date.isoformat() if 
                     task.due_date is not None else None)
                ),
                )

    def load(self) -> list[Task]:
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT title, completed, priority, due_date
                FROM tasks
                ORDER BY id
                """
            )
            rows = cursor.fetchall()
        tasks: list[Task] = []

        for title, completed, priority, due_date_value in rows:
            task = Task(title=title, priority=Priority(priority), 
                        due_date=(date.fromisoformat(due_date_value) if due_date_value is not None else None),
                        )
            if bool(completed):
                task.complete()
            tasks.append(task)
        return tasks
    
            
            
