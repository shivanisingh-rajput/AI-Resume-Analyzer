
const form = document.getElementById("analyze-form");
const fileInput = document.getElementById("resume-file");
const uploadArea = document.getElementById("upload-area");
const fileLabel = document.getElementById("file-label");
const fileHint = document.getElementById("file-hint");
const analyzeButton = document.getElementById("analyze-button");
const buttonText = document.getElementById("button-text");
const errorMessage = document.getElementById("error-message");
const resultsSection = document.getElementById("results");

fileInput.addEventListener("change", () => {
    const file = fileInput.files[0];

    if (!file) {
        fileLabel.textContent = "Choose your resume";
        fileHint.textContent = "Drag and drop, or click to browse";
        return;
    }

    fileLabel.textContent = file.name;
    fileHint.textContent = `${(file.size / (1024 * 1024)).toFixed(2)} MB`;
    errorMessage.hidden = true;
});

uploadArea.addEventListener("dragover", (event) => {
    event.preventDefault();
    uploadArea.classList.add("dragging");
});

uploadArea.addEventListener("dragleave", () => {
    uploadArea.classList.remove("dragging");
});

uploadArea.addEventListener("drop", (event) => {
    event.preventDefault();
    uploadArea.classList.remove("dragging");

    const file = event.dataTransfer.files[0];
    if (!file) return;

    const extension = file.name.split(".").pop().toLowerCase();

    if (!["pdf", "docx"].includes(extension)) {
        showError("Please choose a PDF or DOCX file.");
        return;
    }

    const transfer = new DataTransfer();
    transfer.items.add(file);
    fileInput.files = transfer.files;
    fileInput.dispatchEvent(new Event("change"));
});

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    errorMessage.hidden = true;

    const file = fileInput.files[0];
    const jobDescription = document.getElementById("job-description").value.trim();

    if (!file) {
        showError("Please upload your resume.");
        return;
    }

    const extension = file.name.split(".").pop().toLowerCase();

    if (!["pdf", "docx"].includes(extension)) {
        showError("Only PDF and DOCX files are supported.");
        return;
    }

    if (file.size > 10 * 1024 * 1024) {
        showError("Your resume must be smaller than 10 MB.");
        return;
    }

    if (!jobDescription) {
        showError("Please enter a job description.");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("job_description", jobDescription);

    analyzeButton.disabled = true;
    buttonText.textContent = "Analyzing resume...";
    resultsSection.hidden = true;

    try {
        const response = await fetch("/analyze-resume", {
            method: "POST",
            body: formData
        });

        const data = await response.json().catch(() => ({}));

        if (!response.ok) {
            throw new Error(data.detail || `Analysis failed (${response.status}).`);
        }

        renderResults(data);
        resultsSection.hidden = false;
        resultsSection.scrollIntoView({ behavior: "smooth", block: "start" });
    } catch (error) {
        showError(
            error.message || "Unable to analyze your resume. Please try again."
        );
    } finally {
        analyzeButton.disabled = false;
        buttonText.textContent = "Analyze my resume";
    }
});

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.hidden = false;
}

function renderResults(data) {
    const jobMatch = data.job_match || {};

    const resumeSkills = data.skills || [];
    const matchedSkills = jobMatch.matched_skills || [];
    const missingSkills = jobMatch.missing_skills || [];
    const recommendations = data.recommendations || [];

    const matchPercentage = Number(
        jobMatch.match_percentage ?? jobMatch.match_percent ?? 0
    );

    document.getElementById("result-filename").textContent =
        `${data.filename || "Resume"} · ${data.word_count ?? 0} words`;

    document.getElementById("match-percentage").textContent =
        `${Number.isFinite(matchPercentage) ? matchPercentage : 0}%`;

    document.getElementById("match-progress").style.width =
        `${Math.min(100, Math.max(0, matchPercentage))}%`;

    document.getElementById("skill-count").textContent =
        data.skill_count ?? resumeSkills.length;

    document.getElementById("matched-count").textContent =
        jobMatch.matched_count ?? matchedSkills.length;

    document.getElementById("missing-count").textContent =
        jobMatch.missing_count ?? missingSkills.length;

    renderSkillList("resume-skills", resumeSkills, "neutral");
    renderSkillList("matched-skills", matchedSkills, "neutral");
    renderSkillList("missing-skills", missingSkills, "missing");
    renderRecommendations(recommendations);
}

function renderSkillList(elementId, skills, className = "") {
    const container = document.getElementById(elementId);
    container.replaceChildren();

    if (!skills.length) {
        const empty = document.createElement("p");
        empty.className = "empty-state";
        empty.textContent = "No skills to display.";
        container.appendChild(empty);
        return;
    }

    skills.forEach((skill) => {
        const tag = document.createElement("span");
        tag.className = `skill-tag ${className}`.trim();
        tag.textContent = String(skill);
        container.appendChild(tag);
    });
}

function renderRecommendations(recommendations) {
    const container = document.getElementById("recommendations");
    container.replaceChildren();

    if (!recommendations.length) {
        const empty = document.createElement("p");
        empty.className = "empty-state";
        empty.textContent = "No additional recommendations were returned.";
        container.appendChild(empty);
        return;
    }

    recommendations.forEach((item, index) => {
        const card = document.createElement("div");
        card.className = "recommendation";

        const title = document.createElement("strong");
        const description = document.createElement("p");

        if (typeof item === "string") {
            title.textContent = `Recommendation ${index + 1}`;
            description.textContent = item;
        } else {
            title.textContent =
                item.skill || item.title || item.topic ||
                `Recommendation ${index + 1}`;

            description.textContent =
                item.recommendation || item.description ||
                item.action || item.reason ||
                "Review this recommendation and identify a practical next step.";
        }

        card.append(title, description);
        container.appendChild(card);
    });
}

document.getElementById("new-analysis").addEventListener("click", () => {
    form.reset();
    fileLabel.textContent = "Choose your resume";
    fileHint.textContent = "Drag and drop, or click to browse";
    resultsSection.hidden = true;
    errorMessage.hidden = true;
    form.scrollIntoView({ behavior: "smooth", block: "start" });
});
