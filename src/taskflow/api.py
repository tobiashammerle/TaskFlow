from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from taskflow.application_setup import initialize_application
from taskflow.config import load_repository_type
from taskflow.exception_handlers import (
    duplicate_task_handler,
    empty_title_handler,
    task_not_found_handler,
)
from taskflow.exceptions import DuplicateTaskError, EmptyTitleError, TaskNotFoundError
from taskflow.routers.v1 import router as v1_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    repository_type = load_repository_type(Path("settings.ini"))
    initialize_application(repository_type)
    yield


app = FastAPI(lifespan=lifespan)


app.add_exception_handler(TaskNotFoundError, task_not_found_handler)
app.add_exception_handler(DuplicateTaskError, duplicate_task_handler)
app.add_exception_handler(EmptyTitleError, empty_title_handler)

app.include_router(v1_router)


@app.get("/")
def root():
    return {"message": "TaskFlow API läuft"}
