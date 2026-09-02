from fastapi import FastAPI

from taskflow.exception_handlers import (
    duplicate_task_handler,
    empty_title_handler,
    task_not_found_handler,
)
from taskflow.exceptions import DuplicateTaskError, EmptyTitleError, TaskNotFoundError
from taskflow.routers.tasks import router as tasks_router

app = FastAPI()


app.add_exception_handler(TaskNotFoundError, task_not_found_handler)
app.add_exception_handler(DuplicateTaskError, duplicate_task_handler)
app.add_exception_handler(EmptyTitleError, empty_title_handler)

app.include_router(tasks_router)


@app.get("/")
def root():
    return {"message": "TaskFlow API läuft"}
