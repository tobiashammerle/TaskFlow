from unittest.mock import Mock
import taskflow.main as main_module

def test_main_connects_application_components(monkeypatch) -> None:
    repository = Mock()
    task_service = Mock()
    monkeypatch.setattr(main_module,
                         "configure_logging",
                         Mock())
    monkeypatch.setattr(main_module,
                        "create_repository",
                        Mock(return_value=repository),
    )
    monkeypatch.setattr(main_module,
                        "TaskService",
                        Mock(return_value=task_service),
    )
    monkeypatch.setattr(main_module,
                        "run_cli", Mock())
    main_module.main()

    main_module.create_repository.assert_called_once_with()
    main_module.TaskService.assert_called_once_with(repository)
    main_module.run_cli.assert_called_once_with(task_service)
