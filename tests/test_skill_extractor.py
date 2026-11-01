
import unittest

from modules.skill_extractor import extract_skills


class TestSkillExtractor(unittest.TestCase):

    def test_extract_multiple_skills(self):
        text = "I know Python, SQL, Pandas and Machine Learning."

        result = extract_skills(text)

        self.assertIn("Python", result)
        self.assertIn("SQL", result)
        self.assertIn("Pandas", result)
        self.assertIn("Machine Learning", result)

    def test_case_insensitive_matching(self):
        result = extract_skills("PYTHON and pandas")

        self.assertIn("Python", result)
        self.assertIn("Pandas", result)

    def test_empty_text(self):
        self.assertEqual(extract_skills(""), [])

    def test_no_skills(self):
        self.assertEqual(
            extract_skills("I enjoy reading books."),
            []
        )

    def test_avoid_partial_word_match(self):
        result = extract_skills("The word pythonic is present.")

        self.assertNotIn("Python", result)


if __name__ == "__main__":
    unittest.main()
