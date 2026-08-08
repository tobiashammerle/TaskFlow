import pytest
from pathlib import Path
from taskflow.config import load_repository_type
from taskflow.repository_type import RepositoryType
from taskflow.exceptions import ConfigurationError

def test_load_repository_type_returns_sqlite(tmp_path: Path) -> None:
    # Arrange
    config_file = tmp_path / "settings.ini"
    config_file.write_text("[repository]\n"
                           "type = sqlite\n",
                           encoding="utf-8")
    # Act
    repository_type = load_repository_type(config_file)

    # Assert
    assert repository_type == RepositoryType.SQLITE

def test_load_repository_type_raises_configuration_error_for_invalid_value(tmp_path: Path) -> None:
    config_file = tmp_path / "settings.ini"
    config_file.write_text("[repository]\n"
                           "type = sqlit\n",
                           encoding="utf-8")
    with pytest.raises(ConfigurationError):
        load_repository_type(config_file)

def test_load_repository_type_raises_configuration_error_for_missing_key(tmp_path: Path) -> None:
    config_file = tmp_path / "settings.ini"
    config_file.write_text("[database]\n"
                           "type = sqlite\n",
                           encoding="utf-8")
    with pytest.raises(ConfigurationError):
        load_repository_type(config_file)