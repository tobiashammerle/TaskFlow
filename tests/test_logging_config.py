from taskflow.logging_config import configure_logging

def test_configure_logging_creates_log_directory(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    configure_logging()
    assert (tmp_path / "logs").exists()

    