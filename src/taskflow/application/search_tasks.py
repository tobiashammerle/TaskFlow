from taskflow.task import Task


class SearchTasks:
    def execute(self, tasks: list[Task], search_text: str) -> list[Task]:
        normalized_search_text = search_text.strip().casefold()
        return [
            task for task in tasks if normalized_search_text in task.title.casefold()
        ]
