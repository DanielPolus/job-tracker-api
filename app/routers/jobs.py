from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query, Response
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from app.core.deps import get_db
from app.models.job import Job, SeniorityLevel, EmploymentType
from app.models.company import Company
from app.schemas.job import JobCreate, JobRead

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.post("", response_model=JobRead, status_code=status.HTTP_201_CREATED)
def register_job(payload: JobCreate, db: Session = Depends(get_db)):
    company = db.query(Company).get(payload.company_id)
    if not company:
        raise HTTPException(status_code=400, detail="Company not found")

    title_norm = (payload.title or "").strip()

    exists = (
        db.query(Job)
        .filter(
            Job.company_id == payload.company_id,
            func.trim(Job.title) == title_norm
        )
        .first()
    )
    if exists:
        raise HTTPException(status_code=409, detail="Job with this title already exists for the company")

    job = Job(
        title=title_norm,
        company_id=payload.company_id,
        link=str(payload.link) if payload.link else None,  # AnyUrl -> str
        description=payload.description,
        seniority=SeniorityLevel(payload.seniority) if payload.seniority else None,
        employment_type=EmploymentType(payload.employment_type) if payload.employment_type else None,
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

@router.get("", response_model=List[JobRead], status_code=status.HTTP_200_OK)
def list_jobs(
    response: Response,
    db: Session = Depends(get_db),
    q: Optional[str] = Query(None, description="Поиск по title/description"),
    company_id: Optional[int] = Query(None),
    seniority: Optional[str] = Query(None, description="intern|junior|middle|senior"),
    employment_type: Optional[str] = Query(None, description="full_time|part_time|contract|intern"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    query = db.query(Job)

    if q:
        pattern = f"%{q}%"
        query = query.filter(or_(Job.title.ilike(pattern), Job.description.ilike(pattern)))

    if company_id is not None:
        query = query.filter(Job.company_id == company_id)

    if seniority:
        try:
            query = query.filter(Job.seniority == SeniorityLevel(seniority))
        except ValueError:
            raise HTTPException(status_code=422, detail="Invalid seniority")

    if employment_type:
        try:
            query = query.filter(Job.employment_type == EmploymentType(employment_type))
        except ValueError:
            raise HTTPException(status_code=422, detail="Invalid employment_type")

    total = query.count()
    items = (
        query.order_by(Job.created_at.desc())
             .limit(limit)
             .offset(offset)
             .all()
    )
    response.headers["X-Total-Count"] = str(total)
    return items

@router.get("/{job_id}", response_model=JobRead, status_code=status.HTTP_200_OK)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
