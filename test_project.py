import unittest

from student import Student
from results import assign_grade, calculate_average, calculate_total, result_summary, validate_score


class ResultTests(unittest.TestCase):
    def test_total_and_average(self):
        scores = {"Mathematics": 80, "English": 70, "Physics": 90, "Chemistry": 60, "Biology": 100}
        self.assertEqual(calculate_total(scores), 400)
        self.assertEqual(calculate_average(scores), 80)

    def test_grade_boundaries(self):
        self.assertEqual(assign_grade(80), "A")
        self.assertEqual(assign_grade(79.99), "B")
        self.assertEqual(assign_grade(70), "B")
        self.assertEqual(assign_grade(49.99), "F")

    def test_pending_until_five_subjects(self):
        self.assertFalse(result_summary({"Math": 90})["complete"])

    def test_score_validation(self):
        self.assertEqual(validate_score("75.5"), 75.5)
        with self.assertRaises(ValueError):
            validate_score(101)

    def test_student_round_trip(self):
        student = Student("st001", "Test Student", "SS1", "Female", "2008-01-02")
        student.add_score("Mathematics", 88)
        restored = Student.from_dict(student.to_dict())
        self.assertEqual(restored.student_id, "ST001")
        self.assertEqual(restored.scores["Mathematics"], 88.0)


if __name__ == "__main__":
    unittest.main()
