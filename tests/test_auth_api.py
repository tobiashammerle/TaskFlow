import pytest
from fastapi.testclient import TestClient

from taskflow.api import app
from taskflow.exceptions import DuplicateUserError, InvalidCredentialsError
from taskflow.routers.dependencies import (
    get_login_user_use_case,
    get_register_user_use_case,
)


class FakeRegisterUser:
    def __init__(self, error: Exception | None = None) -> None:
        self._error = error

    def execute(self, email: str, password: str) -> None:
        if self._error is not None:
            raise self._error


class FakeLoginUser:
    def __init__(self, error: Exception | None = None) -> None:
        self._error = error

    def execute(self, email: str, password: str) -> str:
        if self._error is not None:
            raise self._error
        return "test-token"


@pytest.fixture(autouse=True)
def clear_dependency_overrides():
    yield
    app.dependency_overrides.clear()


def test_register_user_returns_201() -> None:
    app.dependency_overrides[get_register_user_use_case] = lambda: FakeRegisterUser()
    client = TestClient(app)
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "max@example.com",
            "password": "TestPassword123",
        },
    )
    assert response.status_code == 201


def test_register_existing_user_returns_409() -> None:
    app.dependency_overrides[get_register_user_use_case] = lambda: FakeRegisterUser(
        DuplicateUserError("Der User existiert bereits.")
    )
    client = TestClient(app)
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "max@example.com",
            "password": "TestPassword123",
        },
    )
    assert response.status_code == 409


def test_login_returns_access_token() -> None:
    app.dependency_overrides[get_login_user_use_case] = lambda: FakeLoginUser()
    client = TestClient(app)
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "max@example.com",
            "password": "TestPassword123",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "access_token": "test-token",
        "token_type": "bearer",
    }


def test_login_with_invalid_credentials_returns_401() -> None:
    app.dependency_overrides[get_login_user_use_case] = lambda: FakeLoginUser(
        error=InvalidCredentialsError("Ungültige Zugangsdaten.")
    )
    client = TestClient(app)
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "max@example.com",
            "password": "wrong-password",
        },
    )
    assert response.status_code == 401
