from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, AnyUrl, field_validator
from pydantic.config import ConfigDict
from app.models.job import SeniorityLevel, EmploymentType  # 👈 импорт enum'ов

class JobBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=200)
    company_id: int = Field(...)
    link: Optional[AnyUrl] = Field(None)
    description: Optional[str] = Field(None)
    seniority: Optional[SeniorityLevel] = None            # 👈 enum
    employment_type: Optional[EmploymentType] = None      # 👈 enum

class JobCreate(JobBase):
    @field_validator("title", mode="before")
    @classmethod
    def normalize_title(cls, v: str) -> str:
        return v.strip() if isinstance(v, str) else v

class JobRead(JobBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,   # опционально: в JSON уйдут строки, не объекты Enum
    )
