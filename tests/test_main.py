from pathlib import Path
from unittest.mock import Mock

import taskflow.main as main_module
from taskflow.repository_type import RepositoryType


def test_main_connects_application_components(monkeypatch) -> None:
    repository = Mock()
    repository_type = RepositoryType.SQLITE
    load_repository_type_mock = Mock(return_value=repository_type)
    create_task = Mock()
    complete_task = Mock()
    remove_task = Mock()
    get_tasks = Mock()

    create_task_factory = Mock(return_value=create_task)
    complete_task_factory = Mock(return_value=complete_task)
    remove_task_factory = Mock(return_value=remove_task)
    get_tasks_factory = Mock(return_value=get_tasks)
    create_repository_mock = Mock(return_value=repository)
    run_cli_mock = Mock()

    monkeypatch.setattr(main_module, "configure_logging", Mock())
    monkeypatch.setattr(
        main_module,
        "load_repository_type",
        load_repository_type_mock,
    )
    monkeypatch.setattr(
        main_module,
        "create_repository",
        create_repository_mock,
    )
    monkeypatch.setattr(main_module, "run_cli", run_cli_mock)
    monkeypatch.setattr(main_module, "CreateTask", create_task_factory)
    monkeypatch.setattr(main_module, "CompleteTask", complete_task_factory)
    monkeypatch.setattr(main_module, "RemoveTask", remove_task_factory)
    monkeypatch.setattr(main_module, "GetTasks", get_tasks_factory)
    main_module.main()

    load_repository_type_mock.assert_called_once_with(Path("settings.ini"))
    create_repository_mock.assert_called_once_with(repository_type)
    create_task_factory.assert_called_once_with(repository)
    complete_task_factory.assert_called_once_with(repository)
    remove_task_factory.assert_called_once_with(repository)
    get_tasks_factory.assert_called_once_with(repository)
    run_cli_mock.assert_called_once_with(
        create_task, complete_task, remove_task, get_tasks
    )
