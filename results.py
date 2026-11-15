"""Score validation, calculations, and grading rules."""

MINIMUM_SUBJECTS = 5

# Grading scale used by this project. Each score is out of 100.
GRADE_BANDS = (
    (80, "A"),
    (70, "B"),
    (60, "C"),
    (50, "D"),
    (0, "F"),
)


def validate_score(score):
    """Return a score as a float, or raise ValueError if it is invalid."""
    try:
        value = float(score)
    except (TypeError, ValueError):
        raise ValueError("Score must be a number.") from None

    if not 0 <= value <= 100:
        raise ValueError("Score must be between 0 and 100.")
    return value


def calculate_total(scores):
    """Calculate the sum of all recorded subject scores."""
    return sum(float(score) for score in scores.values())


def calculate_average(scores):
    """Calculate the average, returning 0 when no scores exist."""
    if not scores:
        return 0.0
    return calculate_total(scores) / len(scores)


def assign_grade(average):
    """Assign a letter grade using the project's grading scale."""
    for minimum, grade in GRADE_BANDS:
        if average >= minimum:
            return grade
    return "F"


def result_summary(scores):
    """Return total, average, and grade for a score dictionary."""
    if len(scores) < MINIMUM_SUBJECTS:
        return {
            "complete": False,
            "total": calculate_total(scores),
            "average": calculate_average(scores),
            "grade": "Pending",
        }

    average = calculate_average(scores)
    return {
        "complete": True,
        "total": calculate_total(scores),
        "average": average,
        "grade": assign_grade(average),
    }
