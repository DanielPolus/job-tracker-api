from typing import Optional, List
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status, Query, Response
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.core.deps import get_db, get_current_user
from app.models.application import Application, ApplicationStatus
from app.models.job import Job
from app.schemas.application import ApplicationCreate, ApplicationUpdate, ApplicationRead

router = APIRouter(prefix="/applications", tags=["applications"])


@router.post("", response_model=ApplicationRead, status_code=status.HTTP_201_CREATED)
def register_application(
    payload: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    # проверяем, что вакансия существует
    job = db.query(Job).get(payload.job_id)
    if not job:
        raise HTTPException(status_code=400, detail="Job not found")

    # не допускаем дубль (user_id, job_id)
    duplicate = (
        db.query(Application)
        .filter(and_(Application.user_id == current_user.id,
                     Application.job_id == payload.job_id))
        .first()
    )
    if duplicate:
        raise HTTPException(status_code=409, detail="Application already exists for this job")

    application = Application(
        user_id=current_user.id,
        job_id=payload.job_id,
        status=payload.status,
        applied_at=payload.applied_at,
        next_action_date=payload.next_action_date,
        notes=payload.notes,
    )
    db.add(application)
    db.commit()
    db.refresh(application)
    return application


@router.get("", response_model=List[ApplicationRead], status_code=status.HTTP_200_OK)
def list_applications(
    response: Response,
    db: Session = Depends(get_db),
    q: Optional[str] = Query(None, description="Поиск по notes"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user=Depends(get_current_user),
):
    query = db.query(Application).filter(Application.user_id == current_user.id)

    if q:
        pattern = f"%{q}%"
        query = query.filter(Application.notes.ilike(pattern))

    total = query.count()
    items = (
        query.order_by(Application.created_at.desc())  # опечатка была: order_dy
             .limit(limit)
             .offset(offset)
             .all()
    )

    response.headers["X-Total-Count"] = str(total)
    return items


@router.get("/{application_id}", response_model=ApplicationRead, status_code=status.HTTP_200_OK)
def get_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    application = db.query(Application).get(application_id)
    if not application or application.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Application not found")
    return application


@router.patch("/{application_id}", response_model=ApplicationRead, status_code=status.HTTP_200_OK)
def patch_application(
    application_id: int,
    payload: ApplicationUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    application = db.query(Application).get(application_id)
    if not application or application.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Application not found")

    if payload.status is not None:
        application.status = payload.status
    if payload.next_action_date is not None:
        application.next_action_date = payload.next_action_date
    if payload.notes is not None:
        application.notes = payload.notes

    db.commit()
    db.refresh(application)
    return application


@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    application = db.query(Application).get(application_id)
    if not application or application.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Application not found")

    db.delete(application)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
