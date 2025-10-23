from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, AnyUrl, field_validator
from pydantic.config import ConfigDict

class CompanyBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=200)
    industry: Optional[str] = Field(None, max_length=100)
    website: Optional[AnyUrl] = Field(None)

class CompanyCreate(CompanyBase):
    @field_validator("name", mode="before")
    @classmethod
    def normalize_name(cls, v: str) -> str:
        if isinstance(v, str):
            v = v.strip()
            v = v.lower()
        return v

class CompanyRead(CompanyBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
