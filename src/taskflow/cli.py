from datetime import date
from typing import Protocol
from uuid import UUID

from taskflow.exceptions import EmptyTitleError, TaskNotFoundError
from taskflow.priority import Priority
from taskflow.task import Task


class CreateTaskHandler(Protocol):
    def execute(
        self,
        title: str,
        priority: Priority = Priority.MEDIUM,
        due_date: date | None = None,
    ) -> Task: ...


class GetTasksHandler(Protocol):
    def execute(self) -> list[Task]: ...


class CompleteTaskHandler(Protocol):
    def execute(self, task_id: UUID) -> Task: ...


class RemoveTaskHandler(Protocol):
    def execute(self, task_id: UUID) -> Task: ...


def run_cli(
    create_task: CreateTaskHandler,
    complete_task_use_case: CompleteTaskHandler,
    remove_task_use_case: RemoveTaskHandler,
    get_tasks_use_case: GetTasksHandler,
) -> None:
    while True:
        show_menu()
        choice = input("Auswahl: ").strip()
        if choice == "1":
            add_task(create_task)
        elif choice == "2":
            show_tasks(get_tasks_use_case)
        elif choice == "3":
            complete_task(get_tasks_use_case, complete_task_use_case)
        elif choice == "4":
            remove_task(get_tasks_use_case, remove_task_use_case)
        elif choice == "5":
            print("TaskFlow wird beendet. ")
            break
        else:
            print("Ungültige Auswahl. ")


def show_menu() -> None:
    """Zeigt das Hauptmenü an."""
    print()
    print("=====================")
    print("      TaskFlow       ")
    print("=====================")
    print("1. Aufgabe hinzufügen")
    print("2. Aufgabe anzeigen")
    print("3. Aufgabe als erledigt markieren")
    print("4. Aufgabe löschen")
    print("5. Beenden")


def add_task(create_task: CreateTaskHandler) -> None:
    """Fragt eine Aufgabe ab und fügt sie der Liste hinzu"""
    title = input("Titel der Aufgabe: ").strip()
    try:
        create_task.execute(title=title)
    except EmptyTitleError:
        print("Der Titel darf nicht leer sein.")
        return
    print("Aufgabe wurde hinzugefügt. ")


def show_tasks(get_tasks_use_case: GetTasksHandler) -> None:
    """Zeigt alle vorhandenen Aufgaben an."""
    tasks = get_tasks_use_case.execute()
    if not tasks:
        print("Es sind noch keine Aufgaben vorhanden. ")
        return
    print("\nAufgaben:")
    for number, task in enumerate(tasks, start=1):
        print(f"{number}. {task}")


def complete_task(
    get_tasks_use_case: GetTasksHandler, complete_task_use_case: CompleteTaskHandler
) -> None:
    """Liest eine Aufgabennummer ein und markiert die Aufgabe als erledigt."""
    tasks = get_tasks_use_case.execute()
    if not tasks:
        print("Es sind keine weiteren Aufgaben zum Erledigen vorhanden. ")
        return
    show_tasks(get_tasks_use_case)
    task_number = input("Nummer der zu erledigenden Aufgabe: ").strip()

    if not task_number.isdigit():
        print("Bitte gib eine gültige Zahl ein. ")
        return
    task_number_int = int(task_number)
    if task_number_int < 1 or task_number_int > len(tasks):
        print("Bitte gib eine gültige Zahl ein. ")
        return
    try:
        task_index = int(task_number) - 1
        task = tasks[task_index]
        complete_task_use_case.execute(task.id)
    except TaskNotFoundError as error:
        print(error)
        return
    print(f'Aufgabe "{task.title}" wurde als erledigt markiert')


def remove_task(
    get_tasks_use_case: GetTasksHandler, remove_task_use_case: RemoveTaskHandler
) -> None:
    """löscht eine Aufgabe anhand ihrer angezeigten Nummer."""
    tasks = get_tasks_use_case.execute()

    if not tasks:
        print("Es sind keine Aufgaben zum Löschen vorhanden.")
        return
    show_tasks(get_tasks_use_case)
    task_number = input("Nummer der zu löschenden Aufgabe: ").strip()
    if not task_number.isdigit():
        print("Gib eine gültige Zahl ein. ")
        return
    task_number_int = int(task_number)
    if task_number_int < 1 or task_number_int > len(tasks):
        print("Bitte gib eine gültige Zahl ein. ")
        return
    try:
        task_index = task_number_int - 1
        task = tasks[task_index]
        removed_task = remove_task_use_case.execute(task.id)
    except TaskNotFoundError as error:
        print(error)
        return
    print(f'Die Aufgabe "{removed_task.title}" wurde gelöscht.')
