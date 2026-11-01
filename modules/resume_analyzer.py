
from modules.resume_parser import parse_resume
from modules.skill_extractor import extract_skills


def analyze_resume(uploaded_file) -> dict:
    """
    Parse a resume and identify the skills mentioned in it.
    """

    # Step 1: Extract text and file information
    resume_data = parse_resume(uploaded_file)

    # Step 2: Identify skills from the extracted text
    skills = extract_skills(resume_data["cleaned_text"])

    # Step 3: Combine the results
    resume_data["skills"] = skills
    resume_data["skill_count"] = len(skills)

    return resume_data
