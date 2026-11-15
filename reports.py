"""Report-card, class-summary, and text-report generation."""

from datetime import datetime

from results import result_summary, MINIMUM_SUBJECTS


def build_student_report(student):
    """Build a readable individual report card."""
    summary = result_summary(student.scores)
    lines = [
        "=" * 58,
        "                 STUDENT REPORT CARD",
        "=" * 58,
        f"Student ID     : {student.student_id}",
        f"Full Name      : {student.full_name}",
        f"Class/Form     : {student.student_class}",
        f"Gender         : {student.gender}",
        f"Date of Birth  : {student.date_of_birth}",
        "-" * 58,
        "SUBJECT SCORES",
        "-" * 58,
    ]

    if student.scores:
        for subject, score in sorted(student.scores.items()):
            lines.append(f"{subject:<35} {float(score):>8.2f}")
    else:
        lines.append("No scores have been entered.")

    lines.extend([
        "-" * 58,
        f"Total Score    : {summary['total']:.2f}",
        f"Average        : {summary['average']:.2f}",
        f"Grade          : {summary['grade']}",
    ])

    if not summary["complete"]:
        lines.append(
            f"Result Status  : Pending "
            f"({len(student.scores)}/{MINIMUM_SUBJECTS} subjects recorded)"
        )
    else:
        lines.append("Result Status  : Complete")

    lines.append(
        f"Result Entered : {student.result_entered_at or 'Not recorded'}"
    )
    lines.append("=" * 58)
    return "\n".join(lines)


def class_statistics(students):
    """Calculate class-wide highest, lowest, and average student results."""
    completed = [
        (student, result_summary(student.scores))
        for student in students
        if result_summary(student.scores)["complete"]
    ]

    if not completed:
        return None

    highest = max(completed, key=lambda item: item[1]["average"])
    lowest = min(completed, key=lambda item: item[1]["average"])
    class_average = sum(item[1]["average"] for item in completed) / len(completed)

    return {
        "students_with_complete_results": len(completed),
        "highest": highest,
        "lowest": lowest,
        "class_average": class_average,
    }


def build_class_report(students):
    """Build a text report containing all students and class statistics."""
    lines = [
        "=" * 78,
        "                  STUDENT RESULT MANAGEMENT SYSTEM",
        "                         CLASS RESULT REPORT",
        "=" * 78,
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        f"{'ID':<12}{'NAME':<25}{'CLASS':<14}{'TOTAL':>9}{'AVERAGE':>10}{'GRADE':>8}",
        "-" * 78,
    ]

    ordered = sorted(
        students,
        key=lambda student: result_summary(student.scores)["average"],
        reverse=True,
    )

    for student in ordered:
        summary = result_summary(student.scores)
        grade = summary["grade"]
        lines.append(
            f"{student.student_id:<12}"
            f"{student.full_name[:24]:<25}"
            f"{student.student_class[:13]:<14}"
            f"{summary['total']:>9.2f}"
            f"{summary['average']:>10.2f}"
            f"{grade:>8}"
        )

    lines.extend(["", "-" * 78, "CLASS STATISTICS"])
    stats = class_statistics(students)

    if stats:
        high_student, high_result = stats["highest"]
        low_student, low_result = stats["lowest"]
        lines.extend([
            f"Students with complete results: {stats['students_with_complete_results']}",
            f"Highest average: {high_result['average']:.2f} "
            f"({high_student.full_name} - {high_student.student_id})",
            f"Lowest average : {low_result['average']:.2f} "
            f"({low_student.full_name} - {low_student.student_id})",
            f"Class average  : {stats['class_average']:.2f}",
        ])
    else:
        lines.append("No students currently have complete results.")

    lines.append("=" * 78)
    return "\n".join(lines)
