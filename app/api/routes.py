from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Certificate, GenerationJob
from ..schemas import (
    GenerationRequest,
    JobResponse,
    JobStatusResponse,
)
from ..services.job_service import process_generation_job
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
)
from fastapi.responses import FileResponse


router = APIRouter()


@router.post("/jobs", response_model=JobResponse)
def create_generation_job(
    request: GenerationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    try:
        # Create the main generation job
        job = GenerationJob(
            status="pending",
            total_count=len(request.recipients),
            success_count=0,
            failure_count=0,
        )

        db.add(job)
        db.flush()

        # Create one certificate record for each recipient
        for recipient in request.recipients:
            certificate = Certificate(
                job_id=job.id,
                recipient_name=recipient.name,
                recipient_email=recipient.email,
                course_name=request.course_name,
                status="pending",
            )

            db.add(certificate)

        # Save job and certificate records
        db.commit()
        db.refresh(job)

        # Start certificate generation in the background
        background_tasks.add_task(
            process_generation_job,
            job.id,
        )

        return JobResponse(
            job_id=job.id,
            status="processing",
            total_count=job.total_count,
        )

    except Exception as error:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Failed to create generation job: {str(error)}",
        )


@router.get("/jobs/{job_id}", response_model=JobStatusResponse)
def get_job_status(
    job_id: int,
    db: Session = Depends(get_db),
):
    job = db.query(GenerationJob).filter(
        GenerationJob.id == job_id
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Generation job not found",
        )

    # A certificate is considered processed when it either
    # succeeds or fails.
    processed_count = (
        job.success_count +
        job.failure_count
    )

    if job.total_count > 0:
        progress = (
            processed_count / job.total_count
        ) * 100
    else:
        progress = 0

    return JobStatusResponse(
        job_id=job.id,
        status=job.status,
        total_count=job.total_count,
        success_count=job.success_count,
        failure_count=job.failure_count,
        progress=progress,
    )
@router.get("/certificates/{certificate_id}")
def get_certificate(
    certificate_id: int,
    db: Session = Depends(get_db),
):
    certificate = db.query(Certificate).filter(
        Certificate.id == certificate_id
    ).first()

    if not certificate:
        raise HTTPException(
            status_code=404,
            detail="Certificate not found",
        )

    if certificate.status != "completed":
        raise HTTPException(
            status_code=409,
            detail="Certificate is not available yet",
        )

    if not certificate.file_path:
        raise HTTPException(
            status_code=404,
            detail="Certificate file not found",
        )

    return FileResponse(
        path=certificate.file_path,
        media_type="application/pdf",
        filename=f"certificate_{certificate.id}.pdf",
    )