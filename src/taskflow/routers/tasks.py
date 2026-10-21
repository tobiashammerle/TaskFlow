from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from taskflow.application.async_complete_task import AsyncCompleteTask
from taskflow.application.async_create_task import AsyncCreateTask
from taskflow.application.async_get_tasks import AsyncGetTasks
from taskflow.application.async_remove_task import AsyncRemoveTask
from taskflow.filter_type import FilterType
from taskflow.routers.dependencies import (
    get_async_complete_task_use_case,
    get_async_create_task_use_case,
    get_async_get_tasks_use_case,
    get_async_remove_task_use_case,
    get_current_user,
    get_filter_tasks_use_case,
    get_search_tasks_use_case,
    get_sort_tasks_use_case,
)
from taskflow.schemas import CreateTaskRequest, TaskResponse
from taskflow.sort_field import SortField
from taskflow.user import User

router = APIRouter(prefix="/tasks", dependencies=[Depends(get_current_user)])


@router.post("", response_model=TaskResponse, status_code=201)
async def create_task(
    request: CreateTaskRequest,
    current_user: User = Depends(get_current_user),
    use_case: AsyncCreateTask = Depends(get_async_create_task_use_case),
):
    task = await use_case.execute(
        title=request.title,
        owner_id=current_user.id,
        priority=request.priority,
        due_date=request.due_date,
    )
    return task


@router.delete("/{task_id}", status_code=204)
async def delete_task(
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    use_case: AsyncRemoveTask = Depends(get_async_remove_task_use_case),
):
    await use_case.execute(task_id, owner_id=current_user.id)


@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def complete_task(
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    use_case: AsyncCompleteTask = Depends(get_async_complete_task_use_case),
):
    task = await use_case.execute(task_id, owner_id=current_user.id)
    return task


@router.get("", response_model=list[TaskResponse])
async def get_tasks(
    search: str | None = None,
    filter: FilterType | None = None,
    sort: SortField | None = None,
    reverse: bool = False,
    limit: int | None = Query(default=None, ge=0),
    offset: int | None = Query(default=None, ge=0),
    current_user: User = Depends(get_current_user),
    get_tasks_use_case: AsyncGetTasks = Depends(get_async_get_tasks_use_case),
    search_tasks_use_case=Depends(get_search_tasks_use_case),
    filter_tasks_use_case=Depends(get_filter_tasks_use_case),
    sort_tasks_use_case=Depends(get_sort_tasks_use_case),
):
    if reverse and sort is None:
        raise HTTPException(status_code=400, detail="reverse requires sort")
    tasks = await get_tasks_use_case.execute(owner_id=current_user.id)
    if search is not None:
        tasks = search_tasks_use_case.execute(tasks, search)
    if filter is not None:
        tasks = filter_tasks_use_case.execute(tasks, filter)
    if sort is not None:
        tasks = sort_tasks_use_case.execute(tasks, sort, reverse)
    if offset is not None:
        tasks = tasks[offset:]
    if limit is not None:
        tasks = tasks[:limit]
    return tasks
