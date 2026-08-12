class TaskFlowError(Exception):
    """Basisklasse für alle TaskFlow-spezifischen Fehler."""


class EmptyTitleError(TaskFlowError):
    """Der Titel einer Aufgabe darf nicht leer sein."""


class TaskNotFoundError(TaskFlowError):
    """Die angegebene Aufgabe existiert nicht."""


class DuplicateTaskError(TaskFlowError):
    """Die Aufgabe existiert bereits."""


class ConfigurationError(TaskFlowError):
    """Die Anwendungskonfiguration ist ungültig."""
