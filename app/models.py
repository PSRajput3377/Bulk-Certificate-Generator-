from datetime import datetime, UTC

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class GenerationJob(Base):
    __tablename__ = "generation_jobs"

    id = Column(Integer, primary_key=True, index=True)

    status = Column(String, default="pending")

    total_count = Column(Integer, default=0)
    success_count = Column(Integer, default=0)
    failure_count = Column(Integer, default=0)

    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    completed_at = Column(DateTime, nullable=True)

    certificates = relationship(
        "Certificate",
        back_populates="job",
        cascade="all, delete-orphan"
    )


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)

    job_id = Column(
        Integer,
        ForeignKey("generation_jobs.id"),
        nullable=False
    )

    recipient_name = Column(String, nullable=False)
    recipient_email = Column(String, nullable=False)
    course_name = Column(String, nullable=False)

    status = Column(String, default="pending")

    file_path = Column(String, nullable=True)
    error_message = Column(String, nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(UTC))

    job = relationship(
        "GenerationJob",
        back_populates="certificates"
    )