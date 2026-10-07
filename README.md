# Bulk Certificate Generator

A FastAPI-based backend service that generates certificates in bulk from a predefined template.

## Features

- Create a bulk certificate generation job
- Validate recipient data
- Generate certificates as PDF files
- Track job status and progress
- Track success and failure for individual certificates
- Continue processing when one certificate fails
- Retrieve generated certificates
- Automated tests

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- ReportLab
- Pytest

## Project Structure

```text
bulk-certificate-generator/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── api/
│   │   └── routes.py
│   └── services/
│       ├── certificate_service.py
│       └── job_service.py
├── tests/
│   ├── conftest.py
│   ├── test_jobs.py
│   ├── test_validation.py
│   └── test_certificates.py
├── generated_certificates/
├── requirements.txt
├── README.md
└── .gitignore
```
```text
Setup
Create and activate a virtual environment:
python3 -m venv venv
source venv/bin/activate

Install dependencies:
pip install -r requirements.txt

Run the Application
uvicorn app.main:app --reload

The API will run at:
http://127.0.0.1:8000

Swagger API documentation:
http://127.0.0.1:8000/docs

API Endpoints
Create Generation Job
POST /jobs

Example request:
{
  "course_name": "Python Bootcamp",
  "recipients": [
    {
      "name": "Prashant Singh",
      "email": "prashant@example.com"
    },
    {
      "name": "Rahul Sharma",
      "email": "rahul@example.com"
    }
  ]
}

Example response:
{
  "job_id": 1,
  "status": "processing",
  "total_count": 2
}

Get Job Status
GET /jobs/{job_id}

Example response:
{
  "job_id": 1,
  "status": "completed",
  "total_count": 2,
  "success_count": 2,
  "failure_count": 0,
  "progress": 100.0
}

Retrieve Certificate
GET /certificates/{certificate_id}

Returns the generated certificate as a PDF.
Validation
The API validates:
- Recipient name
- Recipient email
- Course name
- Number of recipients
Invalid input returns HTTP 422.
Failure Handling
Each certificate is processed independently.
If one certificate fails, the remaining certificates continue processing.
For example:
Certificate 1 → Success
Certificate 2 → Failed
Certificate 3 → Success

The job will be marked as:
completed_with_errors

and the failure reason is stored for the failed certificate.
Testing
Run the test suite:
pytest

The tests cover:
- Job creation
- Input validation
- Certificate generation
- Job progress
- Individual certificate failure
- Certificate retrieval
- Missing certificate handling
Current test result:
9 passed

EOF

This version is much better for the assignment: **short, factual, and focused only on what you actually implemented.
```
