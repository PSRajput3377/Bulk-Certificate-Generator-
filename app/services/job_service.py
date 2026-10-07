from datetime import datetime, UTC

from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..models import Certificate, GenerationJob
from .certificate_service import generate_certificate


def process_generation_job(
    job_id: int,
    db: Session | None = None,
):
    """
    Process all certificates belonging to a generation job.

    In production, the worker creates its own database session.
    Tests can provide their own database session.
    """

    owns_session = db is None

    if owns_session:
        db = SessionLocal()

    try:
        job = (
            db.query(GenerationJob)
            .filter(GenerationJob.id == job_id)
            .first()
        )

        if not job:
            return

        job.status = "processing"
        db.commit()

        certificates = (
            db.query(Certificate)
            .filter(Certificate.job_id == job_id)
            .all()
        )

        for certificate in certificates:
            try:
                certificate.status = "processing"
                db.commit()

                file_path = generate_certificate(
                    certificate_id=certificate.id,
                    recipient_name=certificate.recipient_name,
                    course_name=certificate.course_name,
                )

                certificate.status = "completed"
                certificate.file_path = file_path

                job.success_count += 1

            except Exception as error:
                certificate.status = "failed"
                certificate.error_message = str(error)

                job.failure_count += 1

            finally:
                db.commit()

        # Determine final job status
        if job.failure_count == 0:
            job.status = "completed"
        elif job.success_count == 0:
            job.status = "failed"
        else:
            job.status = "completed_with_errors"

        job.completed_at = datetime.now(UTC)

        db.commit()

    except Exception:
        db.rollback()

        job = (
            db.query(GenerationJob)
            .filter(GenerationJob.id == job_id)
            .first()
        )

        if job:
            job.status = "failed"
            db.commit()

    finally:
        if owns_session:
            db.close()