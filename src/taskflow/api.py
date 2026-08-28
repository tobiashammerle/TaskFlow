from datetime import date

from fastapi import FastAPI
from pydantic import BaseModel

from taskflow.main import build_use_cases
from taskflow.priority import Priority

app = FastAPI()

create_task_use_case, _, _, _ = build_use_cases()


@app.get("/")
def root():
    return {"message": "TaskFlow API läuft"}


class CreateTaskRequest(BaseModel):
    title: str
    priority: Priority = Priority.MEDIUM
    due_date: date | None = None


@app.post("/tasks")
def create_task(request: CreateTaskRequest):
    task = create_task_use_case.execute(
        title=request.title,
        priority=request.priority,
        due_date=request.due_date,
    )
    return {"title": task.title}
