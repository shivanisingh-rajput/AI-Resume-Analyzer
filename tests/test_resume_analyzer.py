
import unittest
from io import BytesIO

import fitz
from docx import Document

from modules.resume_analyzer import analyze_resume


class TestResumeAnalyzer(unittest.TestCase):

    def create_docx(self):
        document = Document()
        document.add_paragraph("Candidate Resume")
        document.add_paragraph(
            "Skills: Python, SQL, Pandas, Machine Learning"
        )

        buffer = BytesIO()
        document.save(buffer)
        buffer.seek(0)
        buffer.name = "candidate.docx"

        return buffer

    def create_pdf(self):
        document = fitz.open()
        page = document.new_page()

        page.insert_text(
            (50, 50),
            "Candidate Resume\nSkills: Python, Java, SQL"
        )

        pdf_bytes = document.tobytes()
        document.close()

        buffer = BytesIO(pdf_bytes)
        buffer.name = "candidate.pdf"

        return buffer

    def test_docx_analysis(self):
        result = analyze_resume(self.create_docx())

        self.assertEqual(result["file_type"], "DOCX")
        self.assertIn("Python", result["skills"])
        self.assertIn("SQL", result["skills"])
        self.assertIn("Pandas", result["skills"])
        self.assertIn("Machine Learning", result["skills"])

    def test_pdf_analysis(self):
        result = analyze_resume(self.create_pdf())

        self.assertEqual(result["file_type"], "PDF")
        self.assertIn("Python", result["skills"])
        self.assertIn("Java", result["skills"])

    def test_skill_count(self):
        result = analyze_resume(self.create_docx())

        self.assertEqual(
            result["skill_count"],
            len(result["skills"])
        )


if __name__ == "__main__":
    unittest.main()
