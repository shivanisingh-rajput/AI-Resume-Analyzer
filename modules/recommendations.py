
SKILL_GUIDANCE = {
    "Python": {
        "category": "Programming",
        "action": "Practice Python fundamentals, functions, data structures, and problem-solving."
    },
    "Java": {
        "category": "Programming",
        "action": "Practice object-oriented programming, collections, and exception handling."
    },
    "SQL": {
        "category": "Database",
        "action": "Practice joins, subqueries, aggregation, and window functions."
    },
    "Pandas": {
        "category": "Data Analysis",
        "action": "Practice data cleaning, grouping, merging, and exploratory data analysis."
    },
    "NumPy": {
        "category": "Data Analysis",
        "action": "Practice array operations, broadcasting, indexing, and numerical computations."
    },
    "Matplotlib": {
        "category": "Data Visualization",
        "action": "Build charts that communicate trends, distributions, and relationships."
    },
    "Seaborn": {
        "category": "Data Visualization",
        "action": "Practice statistical plots, correlation heatmaps, and distribution analysis."
    },
    "Scikit-learn": {
        "category": "Machine Learning",
        "action": "Practice preprocessing, model training, evaluation, and cross-validation."
    },
    "Machine Learning": {
        "category": "Machine Learning",
        "action": "Study supervised and unsupervised learning, feature engineering, and evaluation metrics."
    },
    "Deep Learning": {
        "category": "Deep Learning",
        "action": "Learn neural networks, backpropagation, and training with a deep-learning framework."
    },
    "TensorFlow": {
        "category": "Deep Learning",
        "action": "Build and evaluate neural network models using TensorFlow."
    },
    "PyTorch": {
        "category": "Deep Learning",
        "action": "Practice tensors, autograd, model building, and training loops."
    },
    "Natural Language Processing": {
        "category": "NLP",
        "action": "Practice text preprocessing, tokenization, text classification, and embeddings."
    },
    "Computer Vision": {
        "category": "Computer Vision",
        "action": "Practice image preprocessing, feature extraction, and image classification."
    },
    "FastAPI": {
        "category": "Backend Development",
        "action": "Build REST APIs with request validation, error handling, and API documentation."
    },
    "Flask": {
        "category": "Backend Development",
        "action": "Build a small web application with routes, templates, and API endpoints."
    },
    "Django": {
        "category": "Backend Development",
        "action": "Practice models, views, URL routing, authentication, and database integration."
    },
    "Git": {
        "category": "Version Control",
        "action": "Practice commits, branches, merges, and resolving conflicts."
    },
    "Docker": {
        "category": "Deployment",
        "action": "Containerize an application and practice writing Dockerfiles."
    },
    "AWS": {
        "category": "Cloud Computing",
        "action": "Learn cloud fundamentals and deploy a small application using an appropriate AWS service."
    },
    "Communication": {
        "category": "Professional Skills",
        "action": "Practice explaining technical work clearly and presenting project results."
    },
    "Problem Solving": {
        "category": "Professional Skills",
        "action": "Solve problems systematically and explain your reasoning and trade-offs."
    },
}


def generate_recommendations(job_match_result: dict) -> list[dict]:
    """
    Generate learning recommendations from a job match result.
    """

    missing_skills = job_match_result.get("missing_skills", [])

    recommendations = []

    for skill in missing_skills:
        guidance = SKILL_GUIDANCE.get(
            skill,
            {
                "category": "Technical Skill",
                "action": (
                    f"Study the fundamentals of {skill} and build "
                    "a small practical project demonstrating it."
                ),
            },
        )

        recommendations.append({
            "skill": skill,
            "category": guidance["category"],
            "reason": (
                f"{skill} was identified as a required skill "
                "but was not found in the resume's extracted skills."
            ),
            "suggested_action": guidance["action"],
        })

    return recommendations
