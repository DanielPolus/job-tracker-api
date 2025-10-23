from fastapi import FastAPI
from app.routers import users, auth, companies, jobs, applications

app = FastAPI(title="Job Tracker API")

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(companies.router)
app.include_router(jobs.router)
app.include_router(applications.router)

@app.get("/health")
def health():
    return {"status": "ok"}
