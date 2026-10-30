import logging

import pytest

from taskflow.exceptions import ConfigurationError
from taskflow.logging_config import configure_logging


def test_configure_logging_creates_log_directory(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    configure_logging()
    assert (tmp_path / "logs").exists()


def test_configure_logging_rejects_invalid_log_level(monkeypatch):
    monkeypatch.setenv("LOG_LEVEL", "DEBUUG")
    with pytest.raises(ConfigurationError):
        configure_logging()


def test_configure_logging_accepts_valid_log_level(monkeypatch):
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    captured_config = {}

    def fake_basic_config(**kwargs):
        captured_config.update(kwargs)
        monkeypatch.setattr(logging, "basicConfig", fake_basic_config)

        configure_logging()

        assert captured_config["level"] == logging.DEBUG


def test_configure_logging_without_file(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("LOG_TO_FILE", "false")
    captured_config = {}

    def fake_basic_config(**kwargs):
        captured_config.update(kwargs)

    monkeypatch.setattr(logging, "basicConfig", fake_basic_config)
    configure_logging()
    assert not (tmp_path / "logs").exists()
    assert len(captured_config["handlers"]) == 1
    assert isinstance(
        captured_config["handlers"][0],
        logging.StreamHandler,
    )
