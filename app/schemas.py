from pydantic import BaseModel, EmailStr, Field


class Recipient(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr


class GenerationRequest(BaseModel):
    course_name: str = Field(min_length=1, max_length=200)
    recipients: list[Recipient] = Field(
        min_length=1,
        max_length=1000
    )


class JobResponse(BaseModel):
    job_id: int
    status: str
    total_count: int


class JobStatusResponse(BaseModel):
    job_id: int
    status: str
    total_count: int
    success_count: int
    failure_count: int
    progress: float


class CertificateResponse(BaseModel):
    id: int
    recipient_name: str
    recipient_email: str
    status: str
    file_path: str | None = None
    error_message: str | None = None