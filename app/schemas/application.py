from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, Field
from pydantic.config import ConfigDict

from app.models.application import ApplicationStatus


class ApplicationBase(BaseModel):
    job_id: int = Field(..., description="ID вакансии")
    status: Optional[ApplicationStatus] = Field(
        None, description="Статус заявки (по умолчанию applied)"
    )
    applied_at: Optional[datetime] = Field(
        None, description="Когда подана заявка (если не указано — БД поставит now())"
    )
    next_action_date: Optional[date] = Field(
        None, description="Дата следующего действия (follow-up)"
    )
    notes: Optional[str] = Field(None, description="Заметки по заявке")


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(BaseModel):
    status: Optional[ApplicationStatus] = Field(None)
    next_action_date: Optional[date] = Field(None)
    notes: Optional[str] = Field(None)


class ApplicationRead(BaseModel):
    id: int
    user_id: int
    job_id: int
    status: ApplicationStatus
    applied_at: datetime
    next_action_date: Optional[date] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
    )
