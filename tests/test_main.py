from unittest.mock import Mock

import taskflow.main as main_module


def test_main_connects_application_components(monkeypatch) -> None:
    repository = Mock()
    task_service = Mock()
    create_task = Mock()
    complete_task = Mock()
    remove_task = Mock()
    get_tasks = Mock()

    monkeypatch.setattr(main_module, "configure_logging", Mock())
    monkeypatch.setattr(
        main_module,
        "create_repository",
        Mock(return_value=repository),
    )
    monkeypatch.setattr(
        main_module,
        "TaskService",
        Mock(return_value=task_service),
    )
    monkeypatch.setattr(main_module, "run_cli", Mock())
    monkeypatch.setattr(main_module, "CreateTask", Mock(return_value=create_task))
    monkeypatch.setattr(main_module, "CompleteTask", Mock(return_value=complete_task))
    monkeypatch.setattr(main_module, "RemoveTask", Mock(return_value=remove_task))
    monkeypatch.setattr(main_module, "GetTasks", Mock(return_value=get_tasks))
    main_module.main()

    main_module.create_repository.assert_called_once_with()
    main_module.CreateTask.assert_called_once_with(repository)
    main_module.CompleteTask.assert_called_once_with(repository)
    main_module.RemoveTask.assert_called_once_with(repository)
    main_module.GetTasks.assert_called_once_with(repository)
    main_module.run_cli.assert_called_once_with(
        create_task, complete_task, remove_task, get_tasks
    )
