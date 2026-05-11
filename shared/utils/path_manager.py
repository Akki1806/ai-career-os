from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"

RAW_JOBS_DIR = DATA_DIR / "raw_jobs"
FILTERED_JOBS_DIR = DATA_DIR / "filtered_jobs"

LOGS_DIR = PROJECT_ROOT / "logs"


def show_project_paths():
    print(f"PROJECT_ROOT: {PROJECT_ROOT}")
    print(f"RAW_JOBS_DIR: {RAW_JOBS_DIR}")
    print(f"FILTERED_JOBS_DIR: {FILTERED_JOBS_DIR}")
    print(f"LOGS_DIR: {LOGS_DIR}")