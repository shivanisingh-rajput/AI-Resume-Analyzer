
import re
from io import BytesIO
from pathlib import Path

import fitz
from docx import Document


class ResumeParsingError(Exception):
    """Custom exception for resume parsing errors."""
    pass


def clean_text(text: str) -> str:
    """
    Clean extracted resume text.
    Removes unnecessary whitespace and empty lines.
    """

    if not text or not text.strip():
        raise ResumeParsingError(
            "No readable text found in the resume."
        )

    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove unnecessary spaces and tabs
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def extract_pdf_text(file_bytes: bytes) -> tuple[str, int]:
    """Extract text from a PDF resume."""

    try:
        with fitz.open(
            stream=file_bytes,
            filetype="pdf"
        ) as pdf:

            if len(pdf) == 0:
                raise ResumeParsingError("The PDF is empty.")

            pages_text = []

            for page in pdf:
                pages_text.append(page.get_text("text"))

            extracted_text = "\n".join(pages_text)

            return extracted_text, len(pdf)

    except ResumeParsingError:
        raise

    except Exception as error:
        raise ResumeParsingError(
            f"Unable to read PDF: {error}"
        ) from error


def extract_docx_text(file_bytes: bytes) -> tuple[str, int]:
    """Extract text from a DOCX resume, including tables."""

    try:
        document = Document(BytesIO(file_bytes))

        content = []

        # Extract paragraphs
        for paragraph in document.paragraphs:
            if paragraph.text.strip():
                content.append(paragraph.text)

        # Extract table content
        for table in document.tables:
            for row in table.rows:
                row_content = [
                    cell.text.strip() for cell in row.cells
                ]

                content.append(" | ".join(row_content))

        extracted_text = "\n".join(content)

        return extracted_text, 0

    except Exception as error:
        raise ResumeParsingError(
            f"Unable to read DOCX: {error}"
        ) from error


def parse_resume(uploaded_file) -> dict:
    """
    Parse an uploaded PDF or DOCX resume.

    Accepts a Streamlit UploadedFile or
    a file-like object with name and read().
    """

    if uploaded_file is None:
        raise ResumeParsingError("Please upload a resume.")

    filename = getattr(uploaded_file, "name", "")

    if not filename:
        raise ResumeParsingError("Invalid file name.")

    extension = Path(filename).suffix.lower()

    if extension not in [".pdf", ".docx"]:
        raise ResumeParsingError(
            "Unsupported format. Upload PDF or DOCX."
        )

    try:
        uploaded_file.seek(0)
        file_bytes = uploaded_file.read()
    except Exception as error:
        raise ResumeParsingError(
            "Unable to read the uploaded file."
        ) from error

    if not file_bytes:
        raise ResumeParsingError("The uploaded file is empty.")

    # Extract content according to file type
    if extension == ".pdf":
        raw_text, page_count = extract_pdf_text(file_bytes)

    else:
        raw_text, page_count = extract_docx_text(file_bytes)

    # Clean extracted content
    cleaned_text = clean_text(raw_text)

    return {
        "filename": filename,
        "file_type": extension.replace(".", "").upper(),
        "raw_text": raw_text,
        "cleaned_text": cleaned_text,
        "word_count": len(cleaned_text.split()),
        "character_count": len(cleaned_text),
        "page_count": page_count
    }
