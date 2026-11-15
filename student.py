"""Student model for the Student Result Management System."""

from datetime import datetime


class Student:
    """Represents one student and their subject scores."""

    def __init__(
        self,
        student_id,
        full_name,
        student_class,
        gender,
        date_of_birth,
        scores=None,
        result_entered_at=None,
    ):
        self.student_id = str(student_id).strip().upper()
        self.full_name = str(full_name).strip()
        self.student_class = str(student_class).strip()
        self.gender = str(gender).strip()
        self.date_of_birth = str(date_of_birth).strip()
        self.scores = scores if isinstance(scores, dict) else {}
        self.result_entered_at = result_entered_at

    def add_score(self, subject, score):
        """Add or replace a score for a subject."""
        self.scores[str(subject).strip().title()] = float(score)
        self.result_entered_at = datetime.now().isoformat(timespec="seconds")

    def to_dict(self):
        """Convert this student to a JSON-serializable dictionary."""
        return {
            "student_id": self.student_id,
            "full_name": self.full_name,
            "student_class": self.student_class,
            "gender": self.gender,
            "date_of_birth": self.date_of_birth,
            "scores": self.scores,
            "result_entered_at": self.result_entered_at,
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Student from a dictionary loaded from JSON."""
        return cls(
            student_id=data.get("student_id", ""),
            full_name=data.get("full_name", ""),
            student_class=data.get("student_class", ""),
            gender=data.get("gender", ""),
            date_of_birth=data.get("date_of_birth", ""),
            scores=data.get("scores", {}),
            result_entered_at=data.get("result_entered_at"),
        )
