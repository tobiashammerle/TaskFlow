from datetime import date
from uuid import UUID

from pydantic import BaseModel

from taskflow.priority import Priority


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


class RegisterUserRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
