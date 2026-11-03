
import re


# Canonical skill names returned by the extractor.
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
    "Keras",
    "PySpark",
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


# Alternative spellings and abbreviations mapped to canonical names.
SKILL_ALIASES = {
    "Python": ["python 3", "python3"],
    "JavaScript": ["js"],
    "Scikit-learn": [
        "scikit learn",
        "sklearn",
        "scikit learn library",
    ],
    "Machine Learning": ["ml"],
    "Natural Language Processing": ["nlp"],
    "Computer Vision": ["cv"],
    "Generative AI": ["gen ai", "genai"],
    "Large Language Models": ["llm", "llms"],
    "REST API": ["rest apis", "restful api", "restful apis"],
    "PyTorch": ["pytorch framework"],
}


def _matches_term(text: str, term: str) -> bool:
    """Match a complete skill name or abbreviation."""
    pattern = rf"(?<!\w){re.escape(term.casefold())}(?!\w)"
    return re.search(pattern, text.casefold()) is not None


def extract_skills(resume_text: str) -> list[str]:
    """
    Extract recognized skills and return canonical names.

    Matching is case-insensitive and supports configured aliases.
    Results contain each canonical skill at most once.
    """
    if not resume_text or not resume_text.strip():
        return []

    found_skills = []

    for skill in SKILL_KEYWORDS:
        terms = [skill, *SKILL_ALIASES.get(skill, [])]

        if any(_matches_term(resume_text, term) for term in terms):
            found_skills.append(skill)

    return found_skills
