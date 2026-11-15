"""JSON data storage for student records."""

import json
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data"
DATA_FILE = DATA_DIR / "students.json"


def load_students():
    """Load students from JSON. A missing file means an empty register."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            records = json.load(file)
    except json.JSONDecodeError as error:
        raise RuntimeError(
            f"The data file contains invalid JSON: {error}"
        ) from error

    if not isinstance(records, list):
        raise RuntimeError("The data file must contain a JSON list.")

    from student import Student
    return [Student.from_dict(record) for record in records]


def save_students(students):
    """Save all student records to JSON."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    temporary_file = DATA_FILE.with_suffix(".tmp")

    with temporary_file.open("w", encoding="utf-8") as file:
        json.dump(
            [student.to_dict() for student in students],
            file,
            indent=4,
            ensure_ascii=False,
        )

    temporary_file.replace(DATA_FILE)
