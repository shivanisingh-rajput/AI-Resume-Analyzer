
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
    
    def test_javascript_gets_specific_guidance(self):
        recommendations = generate_recommendations({
            "missing_skills": ["JavaScript"]
        })

        self.assertEqual(len(recommendations), 1)
        self.assertEqual(recommendations[0]["skill"], "JavaScript")
        self.assertNotIn(
            "generic",
            recommendations[0]["suggested_action"].lower()
        )

    def test_generative_ai_gets_specific_guidance(self):
        recommendations = generate_recommendations({
            "missing_skills": ["Generative AI"]
        })

        self.assertEqual(len(recommendations), 1)
        self.assertEqual(recommendations[0]["skill"], "Generative AI")
        self.assertNotIn(
            "generic",
            recommendations[0]["suggested_action"].lower()
        )

    def test_power_bi_gets_specific_guidance(self):
        recommendations = generate_recommendations({
            "missing_skills": ["Power BI"]
        })

        self.assertEqual(len(recommendations), 1)
        self.assertEqual(recommendations[0]["skill"], "Power BI")
        self.assertNotIn(
            "generic",
            recommendations[0]["suggested_action"].lower()
        )


if __name__ == "__main__":
    unittest.main()
