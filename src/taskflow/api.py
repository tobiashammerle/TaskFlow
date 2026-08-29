from datetime import date
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

from taskflow.exceptions import DuplicateTaskError, EmptyTitleError, TaskNotFoundError
from taskflow.main import build_use_cases
from taskflow.priority import Priority

app = FastAPI()

create_task_use_case, complete_task_use_case, _, get_tasks_use_case = build_use_cases()


def get_create_task_use_case():
    return create_task_use_case


def get_get_tasks_use_case():
    return get_tasks_use_case


def get_complete_task_use_case():
    return complete_task_use_case


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
def get_tasks(use_case=Depends(get_get_tasks_use_case)):
    tasks = use_case.execute()
    return tasks


@app.patch("/tasks/{task_id}/complete", response_model=TaskResponse)
def complete_task(task_id: UUID, use_case=Depends(get_complete_task_use_case)):
    try:
        task = use_case.execute(task_id)
    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail="Task nicht gefunden.")
    return task
