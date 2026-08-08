from taskflow.logging_config import configure_logging
import logging
from taskflow.repository_factory import create_repository
from taskflow.task_service import TaskService
from taskflow.exceptions import EmptyTitleError
from taskflow.exceptions import TaskNotFoundError, EmptyTitleError



logger = logging.getLogger(__name__)
# repository = SqliteTaskRepository(Path("tasks.db"))
# repository.initialize_database()

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
    """Zeigt alle vorhandenen Aufgaben an. """
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
    try:
        completed_task = task_service.complete_task(int(task_number)-1)
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
        removed_task = task_service.remove_task(int(task_number)-1)
    except TaskNotFoundError as error:
        print(error)
        return
    print(f'Die Aufgabe "{removed_task.title}" wurde gelöscht.')




def main() -> None:
    """Startet die TaskFlow-Anwendung."""
    configure_logging()
    logger.info("TaskFlow gestartet")

    #print ("Willkommen bei TaskFlow!")
    repository = create_repository()

    # repository = JsonTaskRepository(Path("tasks.json"))
    task_service = TaskService(repository)
    
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
            repository.save(task_service.get_tasks())
            logger.info("TaskFlow beendet")
            print("TaskFlow wird beendet. ")
            break
        else:
            print("Ungültige Auswahl. ")    

if __name__ == "__main__":
    main()