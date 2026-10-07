from pathlib import Path

from reportlab.pdfgen import canvas


OUTPUT_DIR = Path("generated_certificates")
OUTPUT_DIR.mkdir(exist_ok=True)


def generate_certificate(
    certificate_id: int,
    recipient_name: str,
    course_name: str,
) -> str:
    """
    Generate a PDF certificate and return its file path.
    """

    file_path = OUTPUT_DIR / f"certificate_{certificate_id}.pdf"

    pdf = canvas.Canvas(str(file_path))

    # Title
    pdf.setFont("Helvetica-Bold", 28)
    pdf.drawCentredString(
        300,
        500,
        "Certificate of Completion"
    )

    # Recipient text
    pdf.setFont("Helvetica", 18)
    pdf.drawCentredString(
        300,
        430,
        "This certificate is presented to"
    )

    # Recipient name
    pdf.setFont("Helvetica-Bold", 24)
    pdf.drawCentredString(
        300,
        380,
        recipient_name
    )

    # Course
    pdf.setFont("Helvetica", 16)
    pdf.drawCentredString(
        300,
        330,
        f"for successfully completing {course_name}"
    )

    pdf.save()

    return str(file_path)