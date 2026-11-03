# AI Resume Analyzer

An AI-assisted web application that analyzes resumes, identifies candidate skills, compares them with a target job description, and recommends skills to improve job alignment.

## Features

- **Resume parsing:** Supports PDF and DOCX files.
- **Skill extraction:** Identifies technical and professional skills from resume content.
- **Resume analysis:** Extracts useful resume information, including word count and detected skills.
- **Job matching:** Compares extracted skills against the requirements in a job description.
- **Skill-gap analysis:** Identifies relevant skills missing from the resume.
- **Learning recommendations:** Provides guidance for developing missing skills.
- **Web interface:** Provides a browser-based interface for submitting resumes and viewing results.
- **REST API:** Exposes endpoints through FastAPI, with interactive API documentation.

## Technology Stack

| Component | Technology |
|---|---|
| Backend | Python, FastAPI |
| ASGI server | Uvicorn |
| Frontend | HTML, CSS, JavaScript |
| PDF processing | PyMuPDF |
| Word document processing | python-docx |
| Input validation | FastAPI and Pydantic |
| Automated testing | pytest |

## Project Structure

```text
AI-Resume-Analyzer/
├── app.py
├── requirements.txt
├── README.md
├── modules/
│   ├── resume_parser.py
│   ├── skill_extractor.py
│   ├── resume_analyzer.py
│   ├── job_matcher.py
│   └── recommendations.py
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
└── tests/
    ├── test_resume_parser.py
    ├── test_skill_extractor.py
    ├── test_resume_analyzer.py
    ├── test_job_matcher.py
    └── test_recommendations.py
```

## Prerequisites

- Python installed on your system.
- Git, if cloning the repository.
- A web browser.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/shivanisingh-rajput/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Start the application

```bash
python -m uvicorn app:app --reload
```

### 5. Open the application

Visit the following addresses in your browser:

- **Web application:** http://127.0.0.1:8000/
- **API documentation:** http://127.0.0.1:8000/docs
- **Health check:** http://127.0.0.1:8000/health

Keep the terminal running while using the application.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Serves the web interface |
| GET | `/health` | Checks API availability |
| POST | `/analyze-resume` | Analyzes a resume against a job description |

### Resume Analysis Request

The `/analyze-resume` endpoint accepts multipart form data containing:

- `file`: A PDF or DOCX resume.
- `job_description`: The target job description as text.

The response includes the filename, file type, word count, extracted skills, skill count, job-matching results, and recommendations.

Unsupported file types and empty job descriptions are rejected with an appropriate HTTP error.

## Running Tests

Run the complete test suite:

```bash
python -m pytest -v
```

Run a specific test module:

```bash
python -m pytest tests/test_resume_parser.py -v
```

The project has previously passed **38 automated tests** covering resume parsing, skill extraction, job matching, recommendations, and resume analysis. Rerun the tests to verify the current repository state.

## How It Works

1. The user uploads a resume and supplies a target job description.
2. The backend extracts text and relevant information from the resume.
3. The skill extractor identifies and normalizes recognized skills.
4. The job matcher compares candidate skills with recognized job requirements.
5. The recommendation module generates guidance based on the identified skill gaps.
6. The API returns the results for presentation in the web interface.

## Limitations

- Skill extraction depends on the skills and aliases recognized by the application.
- A matching score is an estimate of skill overlap, not a guarantee of job suitability.
- Results depend on the quality and completeness of the resume and job description.
- Recommendations are intended as learning guidance, not a guarantee of employment.

## Future Improvements

- Improve skill recognition and experience analysis.
- Expand job-description parsing and matching explanations.
- Add resume comparison and downloadable reports.
- Improve automated integration testing and deployment.
- Add additional validation against diverse real-world resumes.

## Disclaimer

This application is intended to assist job seekers with resume analysis and skill-gap identification. Its results should not be treated as a definitive hiring decision.

## License

Add a license before distributing the project publicly. Until a license is selected, reuse permissions are not explicitly granted.
