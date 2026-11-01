
import unittest

from modules.job_matcher import match_job


class TestJobMatcher(unittest.TestCase):

    def test_all_skills_match(self):
        result = match_job(
            ["Python", "SQL", "Pandas"],
            "Required skills: Python, SQL, Pandas"
        )

        self.assertEqual(result["match_percentage"], 100.0)
        self.assertEqual(result["matched_skill_count"], 3)
        self.assertEqual(result["missing_skills"], [])

    def test_partial_match(self):
        result = match_job(
            ["Python", "SQL"],
            "Required skills: Python, SQL, Machine Learning"
        )

        self.assertEqual(result["match_percentage"], 66.67)
        self.assertEqual(
            result["missing_skills"],
            ["Machine Learning"]
        )

    def test_no_matching_skills(self):
        result = match_job(
            ["Java"],
            "Required skills: Python, SQL"
        )

        self.assertEqual(result["match_percentage"], 0.0)
        self.assertEqual(
            result["matched_skills"],
            []
        )

    def test_case_insensitive_matching(self):
        result = match_job(
            ["python", "sql"],
            "Required skills: Python, SQL"
        )

        self.assertEqual(result["match_percentage"], 100.0)

    def test_empty_job_description(self):
        with self.assertRaises(ValueError):
            match_job(["Python"], "")

    def test_no_recognized_required_skills(self):
        result = match_job(
            ["Python"],
            "The candidate should have industry experience."
        )

        self.assertEqual(result["total_required_skills"], 0)
        self.assertEqual(result["match_percentage"], 0.0)


if __name__ == "__main__":
    unittest.main()
