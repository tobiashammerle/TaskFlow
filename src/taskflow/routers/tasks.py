from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from taskflow.filter_type import FilterType
from taskflow.routers.dependencies import (
    get_complete_task_use_case,
    get_create_task_use_case,
    get_current_user,
    get_filter_tasks_use_case,
    get_get_tasks_use_case,
    get_remove_task_use_case,
    get_search_tasks_use_case,
    get_sort_tasks_use_case,
)
from taskflow.schemas import CreateTaskRequest, TaskResponse
from taskflow.sort_field import SortField
from taskflow.user import User

router = APIRouter(prefix="/tasks", dependencies=[Depends(get_current_user)])


@router.post("", response_model=TaskResponse, status_code=201)
def create_task(
    request: CreateTaskRequest,
    current_user: User = Depends(get_current_user),
    use_case=Depends(get_create_task_use_case),
):
    task = use_case.execute(
        title=request.title,
        owner_id=current_user.id,
        priority=request.priority,
        due_date=request.due_date,
    )
    return task


@router.delete("/{task_id}", status_code=204)
def delete_task(
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    use_case=Depends(get_remove_task_use_case),
):
    use_case.execute(task_id, owner_id=current_user.id)


@router.patch("/{task_id}/complete", response_model=TaskResponse)
def complete_task(
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    use_case=Depends(get_complete_task_use_case),
):
    task = use_case.execute(task_id, owner_id=current_user.id)
    return task


@router.get("", response_model=list[TaskResponse])
def get_tasks(
    search: str | None = None,
    filter: FilterType | None = None,
    sort: SortField | None = None,
    reverse: bool = False,
    limit: int | None = Query(default=None, ge=0),
    offset: int | None = Query(default=None, ge=0),
    current_user: User = Depends(get_current_user),
    get_tasks_use_case=Depends(get_get_tasks_use_case),
    search_tasks_use_case=Depends(get_search_tasks_use_case),
    filter_tasks_use_case=Depends(get_filter_tasks_use_case),
    sort_tasks_use_case=Depends(get_sort_tasks_use_case),
):
    if reverse and sort is None:
        raise HTTPException(status_code=400, detail="reverse requires sort")
    tasks = get_tasks_use_case.execute(owner_id=current_user.id)
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
