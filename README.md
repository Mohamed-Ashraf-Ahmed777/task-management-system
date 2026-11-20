# Task Management System

A full-stack task management application with a **FastAPI** backend, **PostgreSQL** database, **SQLAlchemy 2.0**, **Alembic** migrations, **JWT** authentication, **Argon2** password hashing, and a lightweight single-file web UI (`HTML/CSS/JS`) served directly at `/ui`.

## Key Features

- **Authentication & Security**: User registration and JWT-based login with Argon2 password hashing and owner-scoped data access on the backend.
- **Task CRUD & Filtering**: Create tasks with optional descriptions, toggle completion status, edit tasks, delete tasks, and filter views by **All**, **Active**, or **Completed**.
- **Built-in Web UI (`/ui`)**: Served directly via FastAPI `FileResponse` from `backend/static/index.html` with zero external frontend build overhead and no CORS friction.
- **Database Migrations**: Schema management handled with SQLAlchemy 2.0 and Alembic.

## Tech Stack

- **Backend**: FastAPI, Uvicorn, Pydantic
- **Database & ORM**: PostgreSQL, SQLAlchemy 2.0, Alembic
- **Auth & Security**: JWT, Argon2
- **Frontend**: Single-file HTML5, CSS3, Vanilla JavaScript

## Project Structure

```text
task-management-system/
├── backend/
│   ├── alembic/
│   ├── app/
│   │   ├── api/
│   │   │   └── routers/
│   │   │       ├── auth.py
│   │   │       ├── tasks.py
│   │   │       └── users.py
│   │   ├── core/
│   │   │       ├── config.py
│   │   │       └── security.py
│   │   ├── crud/
│   │   ├── database/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── deps.py
│   │   └── main.py
│   ├── static/
│   │   └── index.html
│   ├── alembic.ini
│   └── requirements.txt
├── screenshots/
└── README.md
```

## UI Preview

### Authentication & Task Workflow
![Task Completed](screenshots/task-completed.png)

## Local Setup & Run

### 1. Clone the Repository
```bash
git clone [https://github.com/Mohamed-Ashraf-Ahmed777/task-management-system.git](https://github.com/Mohamed-Ashraf-Ahmed777/task-management-system.git)
cd task-management-system
```

### 2. Create & Activate Virtual Environment (Windows PowerShell)
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Configure Environment & Run Migrations
Configure your database and JWT settings in `.env` inside `backend/`, ensure PostgreSQL is running, then apply migrations:
```powershell
alembic upgrade head
```

### 4. Start the Server
```powershell
uvicorn app.main:app --reload
```

- **API Root**: `http://127.0.0.1:8000/`
- **Interactive Web UI**: `http://127.0.0.1:8000/ui`