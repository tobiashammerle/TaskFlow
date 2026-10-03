from fastapi import APIRouter

from taskflow.routers.auth import router as auth_router
from taskflow.routers.tasks import router as tasks_router

router = APIRouter(prefix="/api/v1")
router.include_router(tasks_router)
router.include_router(auth_router)
