from fastapi import FastAPI

from taskflow.routers.tasks import router as tasks_router

app = FastAPI()

app.include_router(tasks_router)


@app.get("/")
def root():
    return {"message": "TaskFlow API läuft"}
