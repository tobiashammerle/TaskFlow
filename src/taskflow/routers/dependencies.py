from taskflow.main import build_use_cases

(
    create_task_use_case,
    complete_task_use_case,
    remove_task_use_case,
    get_tasks_use_case,
    search_tasks_use_case,
    filter_tasks_use_case,
    sort_tasks_use_case,
) = build_use_cases()


def get_create_task_use_case():
    return create_task_use_case


def get_remove_task_use_case():
    return remove_task_use_case


def get_get_tasks_use_case():
    return get_tasks_use_case


def get_complete_task_use_case():
    return complete_task_use_case


def get_search_tasks_use_case():
    return search_tasks_use_case


def get_filter_tasks_use_case():
    return filter_tasks_use_case


def get_sort_tasks_use_case():
    return sort_tasks_use_case
