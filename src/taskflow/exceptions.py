class TaskFlowError(Exception):
    """Basisklasse für alle TaskFlow-spezifischen Fehler."""


class InvalidEmailError(Exception):
    """Wird ausgelöst, wenn eine ungültige E-Mail-Adresse verwendet wird."""


class InvalidPasswordError(Exception):
    """Wird ausgelöst, wenn ein ungültiges Passwort verwendet wird."""


class DuplicateUserError(Exception):
    """User existiert bereits."""


class EmptyTitleError(TaskFlowError):
    """Der Titel einer Aufgabe darf nicht leer sein."""


class TaskNotFoundError(TaskFlowError):
    """Die angegebene Aufgabe existiert nicht."""


class DuplicateTaskError(TaskFlowError):
    """Die Aufgabe existiert bereits."""


class ConfigurationError(TaskFlowError):
    """Die Anwendungskonfiguration ist ungültig."""


class RepositoryError(TaskFlowError):
    """Fehler beim Zugriff auf ein Task-Repository."""
