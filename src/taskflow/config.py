import configparser
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
