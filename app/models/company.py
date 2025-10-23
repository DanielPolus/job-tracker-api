from sqlalchemy import Column, Integer, String, DateTime, func, text
from sqlalchemy.orm import relationship
from app.db.base import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, index=True)
    industry = Column(String(50))
    website = Column(String(255))
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    jobs = relationship("Job", back_populates="company")

