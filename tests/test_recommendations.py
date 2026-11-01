
import unittest

from modules.recommendations import generate_recommendations


class TestRecommendations(unittest.TestCase):

    def test_recommendations_for_missing_skills(self):
        result = {
            "missing_skills": ["Pandas", "Machine Learning"]
        }

        recommendations = generate_recommendations(result)

        skills = [item["skill"] for item in recommendations]

        self.assertEqual(skills, ["Pandas", "Machine Learning"])
        self.assertEqual(
            recommendations[0]["category"],
            "Data Analysis"
        )
        self.assertTrue(
            recommendations[0]["suggested_action"]
        )

    def test_no_missing_skills(self):
        result = {"missing_skills": []}

        self.assertEqual(
            generate_recommendations(result),
            []
        )

    def test_unknown_skill_gets_generic_guidance(self):
        result = {"missing_skills": ["Specialized Tool X"]}

        recommendations = generate_recommendations(result)

        self.assertEqual(
            recommendations[0]["skill"],
            "Specialized Tool X"
        )
        self.assertIn(
            "Specialized Tool X",
            recommendations[0]["suggested_action"]
        )

    def test_missing_key(self):
        self.assertEqual(generate_recommendations({}), [])


if __name__ == "__main__":
    unittest.main()
