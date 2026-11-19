from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.core.config import settings
from app.database.session import get_db

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

@app.get("/health/db")
def check_db(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"database": "Connected successfully"}