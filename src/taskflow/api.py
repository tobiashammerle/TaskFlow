from datetime import date
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

from taskflow.exceptions import DuplicateTaskError, EmptyTitleError, TaskNotFoundError
from taskflow.filter_type import FilterType
from taskflow.main import build_use_cases
from taskflow.priority import Priority
from taskflow.sort_field import SortField

app = FastAPI()

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


class CreateTaskRequest(BaseModel):
    title: str
    priority: Priority = Priority.MEDIUM
    due_date: date | None = None


class TaskResponse(BaseModel):
    id: UUID
    title: str
    completed: bool
    priority: Priority
    due_date: date | None


@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(request: CreateTaskRequest, use_case=Depends(get_create_task_use_case)):
    try:
        task = use_case.execute(
            title=request.title,
            priority=request.priority,
            due_date=request.due_date,
        )
    except DuplicateTaskError:
        raise HTTPException(
            status_code=409, detail="Eine Aufgabe mit diesem Titel existiert bereits."
        )
    except EmptyTitleError:
        raise HTTPException(status_code=400, detail="Der Titel darf nicht leer sein.")
    return task


@app.get("/")
def root():
    return {"message": "TaskFlow API läuft"}


@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks(
    search: str | None = None,
    filter: FilterType | None = None,
    sort: SortField | None = None,
    reverse: bool = False,
    get_tasks_use_case=Depends(get_get_tasks_use_case),
    search_tasks_use_case=Depends(get_search_tasks_use_case),
    filter_tasks_use_case=Depends(get_filter_tasks_use_case),
    sort_tasks_use_case=Depends(get_sort_tasks_use_case),
):
    if reverse and sort is None:
        raise HTTPException(status_code=400, detail="reverse requires sort")
    tasks = get_tasks_use_case.execute()
    if search is not None:
        tasks = search_tasks_use_case.execute(tasks, search)
    if filter is not None:
        tasks = filter_tasks_use_case.execute(tasks, filter)
    if sort is not None:
        tasks = sort_tasks_use_case.execute(tasks, sort, reverse)
    return tasks


@app.patch("/tasks/{task_id}/complete", response_model=TaskResponse)
def complete_task(task_id: UUID, use_case=Depends(get_complete_task_use_case)):
    try:
        task = use_case.execute(task_id)
    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail="Task nicht gefunden.")
    return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: UUID, use_case=Depends(get_remove_task_use_case)):
    try:
        use_case.execute(task_id)
    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail="Task nicht gefunden.")
