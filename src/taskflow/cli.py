from taskflow.exceptions import EmptyTitleError, TaskNotFoundError
from taskflow.task_service import TaskService


def run_cli(task_service: TaskService) -> None:
    while True:
        show_menu()
        choice = input("Auswahl: ").strip()
        if choice == "1":
            add_task(task_service)
        elif choice == "2":
            show_tasks(task_service)
        elif choice == "3":
            complete_task(task_service)
        elif choice == "4":
            remove_task(task_service)
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


def add_task(task_service: TaskService) -> None:
    """Fragt eine Aufgabe ab und fügt sie der Liste hinzu"""
    title = input("Titel der Aufgabe: ").strip()
    try:
        task_service.add_task(title)
    except EmptyTitleError:
        print("Der Titel darf nicht leer sein.")
        return
    print("Aufgabe wurde hinzugefügt. ")


def show_tasks(task_service: TaskService) -> None:
    """Zeigt alle vorhandenen Aufgaben an."""
    tasks = task_service.get_tasks()
    if not tasks:
        print("Es sind noch keine Aufgaben vorhanden. ")
        return
    print("\nAufgaben:")
    for number, task in enumerate(tasks, start=1):
        print(f"{number}. {task}")


def complete_task(task_service: TaskService) -> None:
    """Liest eine Aufgabennummer ein und markiert die Aufgabe als erledigt."""
    tasks = task_service.get_tasks()
    if not tasks:
        print("Es sind keine weiteren Aufgaben zum Erledigen vorhanden. ")
        return
    show_tasks(task_service)
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
        completed_task = task_service.complete_task(task.id)
    except TaskNotFoundError as error:
        print(error)
        return
    print(f'Aufgabe "{completed_task.title}" wurde als erledigt markiert')


def remove_task(task_service: TaskService) -> None:
    """löscht eine Aufgabe anhand ihrer angezeigten Nummer."""
    tasks = task_service.get_tasks()

    if not tasks:
        print("Es sind keine Aufgaben zum Löschen vorhanden.")
        return
    show_tasks(task_service)
    task_number = input("Nummer der zu löschenden Aufgabe: ").strip()
    if not task_number.isdigit():
        print("Gib eine gültige Zahl ein. ")
        return
    try:
        removed_task = task_service.remove_task(int(task_number) - 1)
    except TaskNotFoundError as error:
        print(error)
        return
    print(f'Die Aufgabe "{removed_task.title}" wurde gelöscht.')
