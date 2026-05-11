import json
from pathlib import Path


def load_json(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def score_title(job_title: str, target_roles: list[str]) -> float:
    title_lower = job_title.lower()

    for role in target_roles:
        for word in role.lower().split():
            if word in title_lower:
                return 1.0

    return 0.0

def score_skills(job_skills: list[str], profile_skills: list[str]) -> float:
    if not job_skills:
        return 0.5

    job_set = {skill.lower() for skill in job_skills}
    profile_set = {skill.lower() for skill in profile_skills}

    overlap = job_set & profile_set

    return len(overlap) / len(job_set)

def score_salary(
    job_salary_min: float | None,
    profile_min_salary: float,
    tolerance_pct: float
) -> float:

    if job_salary_min is None:
        return 0.5

    if job_salary_min >= profile_min_salary:
        return 1.0

    gap_pct = (
        (profile_min_salary - job_salary_min)
        / profile_min_salary
    ) * 100

    if gap_pct <= tolerance_pct:
        return 0.5

    return 0.0

def score_location(
    job_location: str,
    target_locations: list[str]
) -> float:

    location_lower = job_location.lower()

    for target in target_locations:
        if target.lower() in location_lower:
            return 1.0

    return 0.0

def score_job(job: dict, profile: dict) -> dict:

    title_score = score_title(
        job["title"],
        profile["target_roles"]
    )

    skills_score = score_skills(
        job["required_skills"],
        profile["skills"]
    )

    salary_score = score_salary(
        job["salary_min_lpa"],
        profile["minimum_salary_lpa"],
        profile["salary_tolerance_pct"]
    )

    location_score = score_location(
        job["location"],
        profile["target_locations"]
    )

    total_score = (
        (title_score * 0.35) +
        (skills_score * 0.35) +
        (salary_score * 0.15) +
        (location_score * 0.15)
    )

    return {
        "job_id": job["id"],
        "title": job["title"],
        "company": job["company"],
        "total_score": round(total_score, 2),
        "send_to_ai": total_score >= 0.6
    }