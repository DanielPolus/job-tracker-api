from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum, func
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class SeniorityLevel(enum.Enum):
    intern = "intern"
    junior = "junior"
    middle = "middle"
    senior = "senior"

class EmploymentType(enum.Enum):
    full_time = "full_time"
    part_time = "part_time"
    contract = "contract"
    intern = "intern"

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="RESTRICT"), nullable=False)
    link = Column(String(255))
    description = Column(Text)
    seniority = Column(Enum(SeniorityLevel), nullable=True)
    employment_type = Column(Enum(EmploymentType), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    company = relationship("Company", back_populates="jobs")
    applications = relationship("Application", back_populates="job")
