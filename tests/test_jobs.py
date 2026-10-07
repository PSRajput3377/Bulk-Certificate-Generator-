from unittest.mock import patch

from app.models import Certificate, GenerationJob


def test_create_generation_job(client):
    response = client.post(
        "/jobs",
        json={
            "course_name": "Python Bootcamp",
            "recipients": [
                {
                    "name": "Prashant Singh",
                    "email": "prashant@example.com",
                },
                {
                    "name": "Rahul Sharma",
                    "email": "rahul@example.com",
                },
            ],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "job_id" in data
    assert data["status"] == "processing"
    assert data["total_count"] == 2


def test_individual_certificate_failure(client, db):
    response = client.post(
        "/jobs",
        json={
            "course_name": "Python Bootcamp",
            "recipients": [
                {
                    "name": "Prashant Singh",
                    "email": "prashant@example.com",
                },
                {
                    "name": "Rahul Sharma",
                    "email": "rahul@example.com",
                },
                {
                    "name": "Priya Singh",
                    "email": "priya@example.com",
                },
            ],
        },
    )

    assert response.status_code == 200

    job_id = response.json()["job_id"]

    certificates = (
        db.query(Certificate)
        .filter(Certificate.job_id == job_id)
        .order_by(Certificate.id)
        .all()
    )

    assert len(certificates) == 3

    def generate_with_one_failure(
        certificate_id,
        recipient_name,
        course_name,
    ):
        if recipient_name == "Rahul Sharma":
            raise RuntimeError(
                "Simulated certificate generation failure"
            )

        return f"generated_certificates/test_{certificate_id}.pdf"

    with patch(
        "app.services.job_service.generate_certificate",
        side_effect=generate_with_one_failure,
    ):
        from app.services.job_service import process_generation_job

        process_generation_job(job_id, db)

    db.expire_all()

    job = (
        db.query(GenerationJob)
        .filter_by(id=job_id)
        .first()
    )

    assert job.status == "completed_with_errors"
    assert job.total_count == 3
    assert job.success_count == 2
    assert job.failure_count == 1

    assert job.success_count + job.failure_count == job.total_count

    failed_certificate = (
        db.query(Certificate)
        .filter(
            Certificate.job_id == job_id,
            Certificate.recipient_name == "Rahul Sharma",
        )
        .first()
    )

    assert failed_certificate is not None
    assert failed_certificate.status == "failed"
    assert (
        failed_certificate.error_message
        == "Simulated certificate generation failure"
    )