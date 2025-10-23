from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query, Response
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from app.core.deps import get_db
from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyRead

router = APIRouter(prefix="/companies", tags=["companies"])

@router.post("", response_model=CompanyRead, status_code=status.HTTP_201_CREATED)
def register_company(payload: CompanyCreate, db: Session = Depends(get_db)):
    name_norm = (payload.name or "").strip().lower()

    exists = (
        db.query(Company)
        .filter(func.lower(Company.name) == name_norm)
        .first()
    )
    if exists:
        raise HTTPException(status_code=409, detail="Company with this name already exists")

    company = Company(
        name=name_norm,
        industry=payload.industry,
        website=str(payload.website) if payload.website else None,
    )
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


@router.get("", response_model=List[CompanyRead], status_code=status.HTTP_200_OK)
def list_companies(
    response: Response,
    db: Session = Depends(get_db),
    q: Optional[str] = Query(None, description="Поиск по name/industry"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    query = db.query(Company)
    if q:
        pattern = f"%{q}%"
        query = query.filter(or_(Company.name.ilike(pattern), Company.industry.ilike(pattern)))
    total = query.count()
    items = (
        query.order_by(Company.created_at.desc())
             .limit(limit)
             .offset(offset)
             .all()
    )
    response.headers["X-Total-Count"] = str(total)
    return items

@router.get("/{company_id}", response_model=CompanyRead, status_code=status.HTTP_200_OK)
def get_company(company_id: int, db: Session = Depends(get_db)):
    company = db.query(Company).get(company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company
