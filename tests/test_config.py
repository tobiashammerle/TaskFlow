from pathlib import Path
from taskflow.config import load_repository_type
from taskflow.repository_type import RepositoryType

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

