from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError

from taskflow.api import app
from taskflow.readiness import check_database_readiness

READINESS_URL = "/ready"


def fake_database_unavailable() -> bool:
    return False


def test_readiness_endpoint_returns_ok():
    with TestClient(app) as client:
        response = client.get(READINESS_URL)
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readiness_endpoint_returns_503_when_database_unavailable():
    app.dependency_overrides[check_database_readiness] = fake_database_unavailable
    try:
        with TestClient(app) as client:
            response = client.get(READINESS_URL)
            assert response.status_code == 503
    finally:
        app.dependency_overrides.pop(check_database_readiness, None)


@pytest.mark.asyncio
async def test_database_readiness_executes_query():
    connection = AsyncMock()
    mock_engine = MagicMock()

    mock_engine.connect.return_value.__aenter__.return_value = connection

    with patch("taskflow.readiness.engine", mock_engine):
        result = await check_database_readiness()
    assert result is True
    connection.execute.assert_awaited_once()
    sql_statement = connection.execute.await_args.args[0]
    assert str(sql_statement) == "SELECT 1"


@pytest.mark.asyncio
async def test_database_readiness_returns_false_on_connection_error():
    mock_engine = MagicMock()
    mock_engine.connect.side_effect = OperationalError(
        statement="SELECT 1",
        params={},
        orig=Exception("Database unavailable"),
    )
    with patch("taskflow.readiness.engine", mock_engine):
        result = await check_database_readiness()
    assert result is False


@pytest.mark.asyncio
async def test_database_readiness_returns_false_on_query_error():
    connection = AsyncMock()
    mock_engine = MagicMock()
    mock_engine.connect.return_value.__aenter__.return_value = connection
    connection.execute.side_effect = OperationalError(
        statement="SELECT 1",
        params={},
        orig=Exception("Query failed"),
    )
    with patch("taskflow.readiness.engine", mock_engine):
        result = await check_database_readiness()
    assert result is False
    connection.execute.assert_awaited_once()
