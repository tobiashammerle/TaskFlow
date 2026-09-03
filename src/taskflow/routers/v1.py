from fastapi import APIRouter

from taskflow.routers.tasks import router as tasks_router

router = APIRouter(prefix="/api/v1")
router.include_router(tasks_router)
