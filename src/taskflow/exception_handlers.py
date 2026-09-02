from fastapi import Request
from fastapi.responses import JSONResponse


async def task_not_found_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


async def duplicate_task_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=409, content={"detail": str(exc)})


async def empty_title_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=400, content={"detail": str(exc)})
