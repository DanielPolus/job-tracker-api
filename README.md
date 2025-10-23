# 💼 Job Tracker API

FastAPI backend for managing companies, jobs, and applications — with authentication, PostgreSQL storage, and Docker support.

## 📘 Live demo: local only (dev)
## 📚 Docs: http://127.0.0.1:8000/docs

# 🚀 Tech Stack
- Backend

- FastAPI — async web framework

- SQLAlchemy ORM — PostgreSQL models & relationships

- Alembic — database migrations

- Passlib[bcrypt] — password hashing

- Pydantic v2 — schema validation

- Uvicorn — ASGI server

- PostgreSQL 16 — via official Docker image

- SQLAlchemy Core/ORM for queries

- Containerization

- Docker Compose — orchestrates API + PostgreSQL

- .env.docker for in-container configuration

# ✨ Features
## 🔐 Users

- /users — register a new user

- /auth/token — login with username & password

- /users/me — get current user (JWT required)

## 🏢 Companies

- /companies — create new company

- /companies (GET) — list all companies

- /companies/{id} — get specific company

## 💼 Jobs

- /jobs — post new job (linked to a company)

- /jobs (GET) — list/search jobs

- /jobs/{id} — get details

## 🧾 Applications

- /applications — create new application (user + job)

- /applications (GET) — list user’s applications

- /applications/{id} — get or update status

- /applications/{id} (DELETE) — delete

Each resource includes timestamps (created_at, updated_at) and validation via Pydantic models.

# ⚙️ Local Setup
## 1️⃣ Create & activate virtual environment
```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## 2️⃣ Install dependencies
```
pip install -r requirements.txt
```

## 3️⃣ Run locally
```
uvicorn app.main:app --reload
```

## 4️⃣ Open docs
```
http://127.0.0.1:8000/docs
```

# 🐳 Docker Setup
## 1️⃣ Build and run
```
docker compose up --build
```

API available at http://127.0.0.1:8000/docs

## 2️⃣ Environment files
# ⚙️ Environment Files

.env — Local development configuration

.env.docker — Environment for Docker containers

.env.example — Template for other users

# 🗝️ API Summary

-- User & Auth

POST /users — Register user

POST /auth/token — Login (JWT)

GET /users/me — Get current user

-- Companies

POST /companies — Create company

GET /companies — List companies

-- Jobs

POST /jobs — Create job

GET /jobs — List or search jobs

-- Applications

POST /applications — Apply for job

PATCH /applications/{id} — Update application status

DELETE /applications/{id} — Delete application

# 🧩 Models Overview

- User → email, password_hash, role, is_active

- Company → name, industry, website

- Job → title, company_id, seniority, employment_type

- Application → user_id, job_id, status, notes, next_action_date

All related via SQLAlchemy relationships and automatically migrated with Alembic.

# 🧪 Testing
```
pytest -q
```

Covers user registration, authentication, and CRUD for jobs/companies/applications.
