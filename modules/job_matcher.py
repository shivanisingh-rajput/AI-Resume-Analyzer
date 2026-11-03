
from modules.skill_extractor import extract_skills, SKILL_ALIASES


def _normalize_skill(skill: str) -> str:
    """Return the canonical name for a recognized skill or alias."""
    normalized = skill.strip().casefold()

    for canonical_skill in SKILL_ALIASES:
        if normalized == canonical_skill.casefold():
            return canonical_skill.casefold()

        aliases = SKILL_ALIASES[canonical_skill]

        if any(normalized == alias.casefold() for alias in aliases):
            return canonical_skill.casefold()

    return normalized


def match_job(resume_skills: list[str], job_description: str) -> dict:
    """
    Compare resume skills with skills identified in a job description.

    Match percentage = matched required skills / total required skills * 100.
    Skill aliases are normalized before comparison.
    """

    if not job_description or not job_description.strip():
        raise ValueError("Job description cannot be empty.")

    resume_skills = resume_skills or []

    # Extract canonical skill names from the job description.
    required_skills = extract_skills(job_description)

    # Normalize resume skill names, including recognized aliases.
    normalized_resume_skills = {
        _normalize_skill(skill)
        for skill in resume_skills
        if isinstance(skill, str) and skill.strip()
    }

    matched_skills = [
        skill
        for skill in required_skills
        if _normalize_skill(skill) in normalized_resume_skills
    ]

    missing_skills = [
        skill
        for skill in required_skills
        if _normalize_skill(skill) not in normalized_resume_skills
    ]

    total_required = len(required_skills)
    match_percentage = (
        (len(matched_skills) / total_required) * 100
        if total_required
        else 0.0
    )

    return {
        "required_skills": required_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "total_required_skills": total_required,
        "matched_skill_count": len(matched_skills),
        "match_percentage": round(match_percentage, 2),
    }
