from taskflow.application.search_tasks import SearchTasks
from taskflow.task import Task


def test_search_tasks_returns_all_results_from_task_list() -> None:
    tasks = [Task("Python lernen"), Task("Git lernen"), Task("Python üben")]
    search_tasks = SearchTasks()
    found_tasks = search_tasks.execute(tasks, "Python")
    assert len(found_tasks) == 2
    assert found_tasks[0].title == "Python lernen"
    assert found_tasks[1].title == "Python üben"


def test_search_tasks_ignores_whitespaces_and_capitalized_letters_in_search_text() -> (
    None
):
    tasks = [Task("Python lernen"), Task("Git lernen")]
    search_tasks = SearchTasks()
    found_tasks = search_tasks.execute(tasks, "   PYTHON   ")
    assert len(found_tasks) == 1
    assert found_tasks[0].title == "Python lernen"


def test_search_tasks_returns_empty_list_when_no_results_found() -> None:
    tasks = [Task("Python lernen"), Task("Git lernen")]
    search_tasks = SearchTasks()
    found_tasks = search_tasks.execute(tasks, "Docker")
    assert len(found_tasks) == 0
    assert found_tasks == []


def test_search_tasks_with_empty_string_returns_complete_task_list() -> None:
    tasks = [Task("Python lernen"), Task("Git lernen")]
    search_tasks = SearchTasks()
    found_tasks = search_tasks.execute(tasks, "")
    assert len(found_tasks) == 2
    assert found_tasks[0].title == "Python lernen"
    assert found_tasks[1].title == "Git lernen"


def test_search_tasks_with_only_whitespaces_in_search_text_returns_complete_task_list() -> (
    None
):
    tasks = [Task("Python lernen"), Task("Git lernen")]
    search_tasks = SearchTasks()
    found_tasks = search_tasks.execute(tasks, "   ")
    assert len(found_tasks) == 2
    assert found_tasks[0].title == "Python lernen"
    assert found_tasks[1].title == "Git lernen"


def test_search_tasks_does_not_change_original_task_list() -> None:
    tasks = [Task("Python lernen"), Task("Git lernen"), Task("Python üben")]
    search_tasks = SearchTasks()
    search_tasks.execute(tasks, "Python")
    assert len(tasks) == 3
    assert tasks[0].title == "Python lernen"
    assert tasks[1].title == "Git lernen"
    assert tasks[2].title == "Python üben"
