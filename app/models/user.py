from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, text
from app.db.base import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    full_name = Column(String(50), nullable=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    is_active = Column(Boolean, server_default=text("true"), nullable=False)
    role = Column(String(50), server_default=text("'user'"), nullable=False)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    applications = relationship("Application", back_populates="user", cascade="all, delete-orphan")

