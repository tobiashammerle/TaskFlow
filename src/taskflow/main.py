
def show_menu() -> None:
    """Zeigt das Hauptmenü an."""
    print()
    print("=====================")
    print("      TaskFlow       ")
    print("=====================")
    print("1. Aufgabe hinzufügen")
    print("2. Aufgabe anzeigen")
    print("3. Aufgabe löschen")
    print("4. Beenden")

def add_task(tasks: list[str]) -> None:
    """Fragt eine Aufgabe ab und fügt sie der Liste hinzu"""
    title = input("Titel der Aufgabe: ").strip()
    if not title:
        print("Der Titel darf nicht leer sein.")
        return
    tasks.append(title)
    print("Aufgabe wurde hinzugefügt. ")

def show_tasks(tasks: list[str]) -> None:
    """Zeigt alle vorhandenen Aufgaben an. """
    if not tasks:
        print("Es sind noch keine Aufgaben vorhanden. ")
        return
    print("\nAufgaben:")
    for number, task in enumerate(tasks, start=1):
        print(f"{number}. {task}")

def remove_task(tasks: list[str]) -> None:
    """löscht eine Aufgabe anhand ihrer angezeigten Nummer."""
    if not tasks:
        print("Es sind keine Aufgaben zum Löschen vorhanden.")
        return
    show_tasks(tasks)
    task_number = input("Nummer der zu löschenden Aufgabe: ").strip()
    if not task_number.isdigit():
        print("Gib eine gültige Zahl ein. ")
        return
    index = int(task_number)-1
    if index < 0 or index >= len(tasks):
        print("Diese Aufgabennummer existiert nicht. ")
        return
    removed_task = tasks.pop(index)
    print(f'Die Aufgabe "{removed_task}" wurde gelöscht.')

def main() -> None:
    """Startet die TaskFlow-Anwendung."""
    print ("Willkommen bei TaskFlow!")
    tasks: list[str] = []
    while True:
        show_menu()
        choice = input("Auswahl: ").strip()
        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            show_tasks(tasks)
        elif choice == "3":
            remove_task(tasks)
        elif choice == "4":
            print("TaskFlow wird beendet. ")
            break
        else:
            print("Ungültige Auswahl. ")    

if __name__ == "__main__":
    main()