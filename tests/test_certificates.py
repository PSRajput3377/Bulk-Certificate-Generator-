from pathlib import Path

from app.models import Certificate
from app.services.job_service import process_generation_job


def test_certificate_generation(client, db):
    response = client.post(
        "/jobs",
        json={
            "course_name": "Python Bootcamp",
            "recipients": [
                {
                    "name": "Prashant Singh",
                    "email": "prashant@example.com",
                },
            ],
        },
    )

    assert response.status_code == 200

    job_id = response.json()["job_id"]

    # Run the worker explicitly.
    process_generation_job(job_id, db)

    status_response = client.get(f"/jobs/{job_id}")

    assert status_response.status_code == 200

    job_data = status_response.json()

    assert job_data["status"] == "completed"
    assert job_data["total_count"] == 1
    assert job_data["success_count"] == 1
    assert job_data["failure_count"] == 0
    assert job_data["progress"] == 100


def test_retrieve_generated_certificate(client, db):
    response = client.post(
        "/jobs",
        json={
            "course_name": "Python Bootcamp",
            "recipients": [
                {
                    "name": "Prashant Singh",
                    "email": "prashant@example.com",
                },
            ],
        },
    )

    assert response.status_code == 200

    job_id = response.json()["job_id"]

    # Explicitly process the job.
    process_generation_job(job_id, db)

    certificate = (
        db.query(Certificate)
        .filter(Certificate.job_id == job_id)
        .first()
    )

    assert certificate is not None
    assert certificate.status == "completed"
    assert certificate.file_path is not None

    # Verify that the PDF exists.
    assert Path(certificate.file_path).exists()

    # Retrieve the generated PDF.
    certificate_response = client.get(
        f"/certificates/{certificate.id}"
    )

    assert certificate_response.status_code == 200
    assert (
        certificate_response.headers["content-type"]
        == "application/pdf"
    )


def test_retrieve_missing_certificate(client):
    response = client.get("/certificates/999999")

    assert response.status_code == 404