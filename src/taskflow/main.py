
def show_menu() -> None:
    """Zeigt das Hauptmenü an."""
    print()
    print("=====================")
    print("      TaskFlow       ")
    print("=====================")
    print("1. Aufgabe hinzufügen")
    print("2. Aufgabe anzeigen")
    print("3. Beenden")

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
            print("TaskFlow wird beendet. ")
            break
        else:
            print("Ungültige Auswahl. ")    

if __name__ == "__main__":
    main()