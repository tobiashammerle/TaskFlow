from pathlib import Path

import pytest

from taskflow.config import (
    load_access_token_expire_minutes,
    load_jwt_secret,
    load_repository_type,
)
from taskflow.exceptions import ConfigurationError
from taskflow.repository_type import RepositoryType


def test_load_repository_type_returns_sqlite(tmp_path: Path) -> None:
    # Arrange
    config_file = tmp_path / "settings.ini"
    config_file.write_text("[repository]\ntype = sqlite\n", encoding="utf-8")
    # Act
    repository_type = load_repository_type(config_file)

    # Assert
    assert repository_type == RepositoryType.SQLITE


def test_load_repository_type_raises_configuration_error_for_invalid_value(
    tmp_path: Path,
) -> None:
    config_file = tmp_path / "settings.ini"
    config_file.write_text("[repository]\ntype = sqlit\n", encoding="utf-8")
    with pytest.raises(ConfigurationError):
        load_repository_type(config_file)


def test_load_repository_type_raises_configuration_error_for_missing_key(
    tmp_path: Path,
) -> None:
    config_file = tmp_path / "settings.ini"
    config_file.write_text("[database]\ntype = sqlite\n", encoding="utf-8")
    with pytest.raises(ConfigurationError):
        load_repository_type(config_file)


def test_load_repository_type_returns_sqlalchemy(tmp_path: Path) -> None:
    # Arrange
    config_file = tmp_path / "settings.ini"
    config_file.write_text("[repository]\ntype = sqlalchemy\n", encoding="utf-8")
    # Act
    repository_type = load_repository_type(config_file)

    # Assert
    assert repository_type == RepositoryType.SQLALCHEMY


def test_load_jwt_secret_rejects_empty_value(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("JWT_SECRET", "")
    with pytest.raises(ConfigurationError):
        load_jwt_secret()


def test_load_access_token_expire_minutes_rejects_negative_value(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("ACCESS_TOKEN_EXPIRE_MINUTES", "-10")
    with pytest.raises(ConfigurationError):
        load_access_token_expire_minutes()


def test_load_access_token_expire_minutes_rejects_zero(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("ACCESS_TOKEN_EXPIRE_MINUTES", "0")
    with pytest.raises(ConfigurationError):
        load_access_token_expire_minutes()
