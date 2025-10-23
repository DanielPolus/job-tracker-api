from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from pydantic.config import ConfigDict

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Plain password (will be hashed)")

class UserRead(UserBase):
    id: int
    role: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
