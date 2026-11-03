
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
        self.assertEqual(result["matched_skills"], [])

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

    def test_machine_learning_alias_matches(self):
        result = match_job(
            ["ML"],
            "Required skill: Machine Learning"
        )

        self.assertEqual(
            result["matched_skills"],
            ["Machine Learning"]
        )
        self.assertEqual(result["match_percentage"], 100.0)

    def test_scikit_learn_alias_matches(self):
        result = match_job(
            ["sklearn"],
            "Required skill: Scikit-learn"
        )

        self.assertEqual(
            result["matched_skills"],
            ["Scikit-learn"]
        )
        self.assertEqual(result["match_percentage"], 100.0)

    def test_javascript_does_not_match_java(self):
        result = match_job(
            ["JavaScript"],
            "Required skill: Java"
        )

        self.assertEqual(result["matched_skills"], [])
        self.assertEqual(result["missing_skills"], ["Java"])
        self.assertEqual(result["match_percentage"], 0.0)

    def test_alias_matching_with_partial_match(self):
        result = match_job(
            ["ML", "Python"],
            "Required skills: Machine Learning, Python, Docker"
        )

        self.assertCountEqual(
            result["matched_skills"],
            ["Python", "Machine Learning"]
        )
        self.assertEqual(result["match_percentage"], 66.67)


if __name__ == "__main__":
    unittest.main()
