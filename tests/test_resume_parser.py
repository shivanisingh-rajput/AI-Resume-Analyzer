
import unittest
from io import BytesIO

import fitz
from docx import Document

from modules.resume_parser import (
    parse_resume,
    ResumeParsingError
)


class TestResumeParser(unittest.TestCase):

    def create_docx(self):
        document = Document()
        document.add_paragraph("Shivani Singh")
        document.add_paragraph("Skills: Python, SQL, Machine Learning")

        buffer = BytesIO()
        document.save(buffer)
        buffer.seek(0)
        buffer.name = "sample.docx"

        return buffer

    def create_pdf(self):
        document = fitz.open()
        page = document.new_page()

        page.insert_text(
            (50, 50),
            "Shivani Singh\nSkills: Python, SQL"
        )

        pdf_bytes = document.tobytes()
        document.close()

        buffer = BytesIO(pdf_bytes)
        buffer.name = "sample.pdf"

        return buffer

    def test_docx_parsing(self):
        result = parse_resume(self.create_docx())

        self.assertEqual(result["file_type"], "DOCX")
        self.assertIn("Shivani Singh", result["cleaned_text"])

    def test_pdf_parsing(self):
        result = parse_resume(self.create_pdf())

        self.assertEqual(result["file_type"], "PDF")
        self.assertIn("Shivani Singh", result["cleaned_text"])

    def test_word_count(self):
        result = parse_resume(self.create_docx())

        self.assertGreater(result["word_count"], 0)

    def test_unsupported_file(self):
        file = BytesIO(b"test")
        file.name = "sample.txt"

        with self.assertRaises(ResumeParsingError):
            parse_resume(file)

    def test_empty_file(self):
        file = BytesIO(b"")
        file.name = "empty.pdf"

        with self.assertRaises(ResumeParsingError):
            parse_resume(file)


if __name__ == "__main__":
    unittest.main()
