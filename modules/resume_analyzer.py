
from modules.resume_parser import parse_resume
from modules.skill_extractor import extract_skills


def analyze_resume(uploaded_file, filename: str | None = None):
    """
    Parse a resume and identify the skills mentioned in it.
    """

    # Step 1: Parse the resume only once
    resume_data = parse_resume(
        uploaded_file,
        filename=filename,
    )

    # Step 2: Identify skills from the extracted text
    skills = extract_skills(resume_data["cleaned_text"])

    # Step 3: Add skill information to the result
    resume_data["skills"] = skills
    resume_data["skill_count"] = len(skills)

    return resume_data
