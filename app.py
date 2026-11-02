
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import RedirectResponse

from modules.resume_analyzer import analyze_resume
from modules.job_matcher import match_job
from modules.recommendations import generate_recommendations
from modules.resume_parser import ResumeParsingError


app = FastAPI(
    title="AI Resume Analyzer API",
    description=(
        "Analyze resumes, match skills against job descriptions, "
        "and generate skill-gap recommendations."
    ),
    version="1.0.0",
)


@app.get("/", include_in_schema=False)
def home():
    """Redirect users to the interactive API documentation."""
    return RedirectResponse(url="/docs")


@app.get("/health", tags=["Health"])
def health_check():
    """Check whether the API is running."""
    return {
        "status": "healthy",
        "message": "AI Resume Analyzer API is running.",
    }


@app.post("/analyze-resume", tags=["Resume Analysis"])
async def analyze_resume_endpoint(
    file: UploadFile = File(..., description="Upload a PDF or DOCX resume"),
    job_description: str = Form(..., description="Paste the target job description"),
):
    """Analyze a resume against a job description."""

    filename = file.filename or ""

    if not filename.lower().endswith((".pdf", ".docx")):
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format. Upload a PDF or DOCX file.",
        )

    if not job_description.strip():
        raise HTTPException(
            status_code=400,
            detail="Job description cannot be empty.",
        )

    try:
        resume_result = analyze_uploaded_resume(file)
        match_result = match_job(
            resume_result["skills"],
            job_description,
        )
        recommendations = generate_recommendations(match_result)

        return {
            "filename": resume_result["filename"],
            "file_type": resume_result["file_type"],
            "word_count": resume_result["word_count"],
            "skills": resume_result["skills"],
            "skill_count": resume_result["skill_count"],
            "job_match": match_result,
            "recommendations": recommendations,
        }

    except ResumeParsingError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    finally:
        await file.close()



def analyze_uploaded_resume(file: UploadFile) -> dict:
    """Pass the uploaded file and original filename to the analyzer."""

    file.file.seek(0)

    return analyze_resume(
        file.file,
        filename=file.filename or "",
    )