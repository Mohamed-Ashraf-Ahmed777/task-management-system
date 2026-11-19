from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Task Management System"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "postgresql+psycopg://postgres:postgres@localhost:5432/task_db"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()