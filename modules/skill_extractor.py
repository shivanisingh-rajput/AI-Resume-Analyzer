
import re


# Skills that the extractor can recognize
SKILL_KEYWORDS = [
    "Python",
    "Java",
    "C++",
    "C#",
    "SQL",
    "HTML",
    "CSS",
    "JavaScript",
    "Pandas",
    "NumPy",
    "Matplotlib",
    "Seaborn",
    "Scikit-learn",
    "TensorFlow",
    "PyTorch",
    "Machine Learning",
    "Deep Learning",
    "Data Analysis",
    "Data Science",
    "Natural Language Processing",
    "Computer Vision",
    "Generative AI",
    "Large Language Models",
    "LangChain",
    "Flask",
    "Django",
    "FastAPI",
    "REST API",
    "Git",
    "GitHub",
    "Docker",
    "AWS",
    "Excel",
    "Power BI",
    "Tableau",
    "Communication",
    "Problem Solving",
]


def extract_skills(resume_text: str) -> list[str]:
    """Extract known skills from resume text."""

    if not resume_text or not resume_text.strip():
        return []

    found_skills = []
    normalized_text = resume_text.lower()

    for skill in SKILL_KEYWORDS:
        # Escape special characters such as +, # and .
        escaped_skill = re.escape(skill.lower())

        # Match whole words or phrases, not partial words.
        pattern = rf"(?<!\w){escaped_skill}(?!\w)"

        if re.search(pattern, normalized_text):
            found_skills.append(skill)

    return found_skills
