
import unittest
from modules.skill_extractor import extract_skills


class TestSkillExtractor(unittest.TestCase):

    # Original tests
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

    # New alias and accuracy tests
    def test_recognize_skill_aliases(self):
        result = extract_skills(
            "Experience with ML, NLP, sklearn, JS and LLMs."
        )

        self.assertIn("Machine Learning", result)
        self.assertIn("Natural Language Processing", result)
        self.assertIn("Scikit-learn", result)
        self.assertIn("JavaScript", result)
        self.assertIn("Large Language Models", result)

    def test_normalize_skill_spelling(self):
        result = extract_skills(
            "Used scikit learn and SCikit-learn for modeling."
        )

        self.assertEqual(result.count("Scikit-learn"), 1)

    def test_java_does_not_match_javascript(self):
        result = extract_skills("My frontend skill is JavaScript.")

        self.assertIn("JavaScript", result)
        self.assertNotIn("Java", result)

    def test_ml_does_not_match_inside_a_longer_word(self):
        result = extract_skills("The project uses an XML document.")

        self.assertNotIn("Machine Learning", result)

    def test_extract_new_skills(self):
        result = extract_skills("Used Keras and PySpark.")

        self.assertIn("Keras", result)
        self.assertIn("PySpark", result)
    
    def test_duplicate_mentions_return_one_skill(self):
        result = extract_skills(
            "Python developer. Built projects using PYTHON and Python 3."
        )

        self.assertEqual(result.count("Python"), 1)

    def test_skill_aliases_are_normalized(self):
        result = extract_skills(
            "Experience with Python3, sklearn, and NLP."
        )

        self.assertIn("Python", result)
        self.assertIn("Scikit-learn", result)
        self.assertIn("Natural Language Processing", result)

    def test_unrelated_words_do_not_create_skill_matches(self):
        result = extract_skills(
            "The candidate enjoys teamwork and reading technical books."
        )

        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
