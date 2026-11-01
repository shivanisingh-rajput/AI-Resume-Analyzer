
from modules.skill_extractor import extract_skills


def match_job(resume_skills: list[str], job_description: str) -> dict:
    """
    Compare resume skills against skills identified in a job description.

    Match percentage = matched required skills / total required skills * 100
    """

    if not job_description or not job_description.strip():
        raise ValueError("Job description cannot be empty.")

    if not resume_skills:
        resume_skills = []

    # Identify required skills mentioned in the job description.
    required_skills = extract_skills(job_description)

    # Normalize resume skills for case-insensitive comparison.
    resume_skill_map = {
        skill.casefold(): skill for skill in resume_skills
    }

    matched_skills = [
        skill
        for skill in required_skills
        if skill.casefold() in resume_skill_map
    ]

    missing_skills = [
        skill
        for skill in required_skills
        if skill.casefold() not in resume_skill_map
    ]

    total_required = len(required_skills)

    if total_required == 0:
        match_percentage = 0.0
    else:
        match_percentage = (
            len(matched_skills) / total_required
        ) * 100

    return {
        "required_skills": required_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "total_required_skills": total_required,
        "matched_skill_count": len(matched_skills),
        "match_percentage": round(match_percentage, 2),
    }
