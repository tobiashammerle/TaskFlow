import configparser
import os
from pathlib import Path

from taskflow.exceptions import ConfigurationError
from taskflow.repository_type import RepositoryType


def load_repository_type(file_path: Path) -> RepositoryType:
    config = configparser.ConfigParser()
    config.read(file_path)
    try:
        repository_value = config["repository"]["type"]
        return RepositoryType(repository_value)
    except (KeyError, ValueError) as error:
        raise ConfigurationError("Ungültige Repository-Konfiguration.") from error


def load_jwt_secret() -> str:
    secret = os.getenv("JWT_SECRET")
    if secret is None:
        raise ConfigurationError("JWT_SECRET ist nicht konfiguriert.")
    return secret


def load_access_token_expire_minutes() -> int:
    value = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    try:
        return int(value)
    except ValueError as error:
        raise ConfigurationError(
            "ACCESS_TOKEN_EXPIRE_MINUTES muss eine Ganzzahl sein."
        ) from error
