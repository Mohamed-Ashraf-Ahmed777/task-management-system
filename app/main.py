from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Task Management System API!",
        "status": "Running successfully"
    }