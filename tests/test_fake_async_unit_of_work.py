import pytest

from tests.fakes import FakeAsyncTaskRepository, FakeAsyncUnitOfWork


@pytest.mark.asyncio
async def test_async_unit_of_work_uses_given_repository():
    repository = FakeAsyncTaskRepository()
    uow = FakeAsyncUnitOfWork(repository)

    async with uow:
        assert uow.tasks is repository
        await uow.commit()


@pytest.mark.asyncio
async def test_async_unit_of_work_propagates_exception():
    repository = FakeAsyncTaskRepository()
    uow = FakeAsyncUnitOfWork(repository)
    with pytest.raises(ValueError):
        async with uow:
            raise ValueError("Testfehler")
