from sqlalchemy import (
    Column, Integer, DateTime, Date, ForeignKey,
    Enum as SAEnum, Text, func, UniqueConstraint, Index
)
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class ApplicationStatus(enum.Enum):
    applied = "applied"
    interview = "interview"
    offer = "offer"
    rejected = "rejected"
    hired = "hired"

class Application(Base):
    __tablename__ = "applications"
    __table_args__ = (
        UniqueConstraint("user_id", "job_id", name="uq_application_user_job"),
        Index("ix_applications_status", "status"),
        Index("ix_applications_next_action_date", "next_action_date"),
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),   # можно RESTRICT — по вкусу
        nullable=False,
    )
    job_id = Column(
        Integer,
        ForeignKey("jobs.id", ondelete="RESTRICT"),
        nullable=False,
    )
    status = Column(SAEnum(ApplicationStatus), nullable=False, server_default="applied")
    applied_at = Column(DateTime, server_default=func.now(), nullable=False)
    next_action_date = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship("User", back_populates="applications")
    job = relationship("Job", back_populates="applications")
