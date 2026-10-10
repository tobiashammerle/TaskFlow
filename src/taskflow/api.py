from fastapi import FastAPI

from taskflow.exception_handlers import (
    duplicate_task_handler,
    duplicate_user_handler,
    empty_title_handler,
    invalid_credentials_handler,
    invalid_token_handler,
    task_not_found_handler,
)
from taskflow.exceptions import (
    DuplicateTaskError,
    DuplicateUserError,
    EmptyTitleError,
    InvalidCredentialsError,
    InvalidTokenError,
    TaskNotFoundError,
)
from taskflow.routers.v1 import router as v1_router

app = FastAPI()


app.add_exception_handler(TaskNotFoundError, task_not_found_handler)
app.add_exception_handler(DuplicateTaskError, duplicate_task_handler)
app.add_exception_handler(EmptyTitleError, empty_title_handler)
app.add_exception_handler(DuplicateUserError, duplicate_user_handler)
app.add_exception_handler(InvalidCredentialsError, invalid_credentials_handler)
app.add_exception_handler(InvalidTokenError, invalid_token_handler)

app.include_router(v1_router)


@app.get("/")
def root():
    return {"message": "TaskFlow API läuft"}
