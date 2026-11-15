"""Main menu for the Student Result Management System."""

from datetime import datetime

from reports import (
    build_class_report,
    build_student_report,
    class_statistics,
)
from results import (
    MINIMUM_SUBJECTS,
    calculate_average,
    calculate_total,
    result_summary,
    validate_score,
)
from storage import load_students, save_students


def get_non_empty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty.")


def get_date_of_birth(prompt="Date of birth (YYYY-MM-DD): "):
    while True:
        value = input(prompt).strip()
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            print("Enter a valid date in YYYY-MM-DD format.")


def find_student(students, student_id):
    target = student_id.strip().upper()
    for student in students:
        if student.student_id == target:
            return student
    return None


def choose_student(students):
    student_id = input("Enter student ID: ").strip()
    student = find_student(students, student_id)
    if student is None:
        print("Student not found.")
    return student


def register_student(students):
    print("\n--- REGISTER NEW STUDENT ---")
    student_id = get_non_empty("Student ID: ").upper()

    if find_student(students, student_id):
        print("A student with that ID already exists.")
        return

    full_name = get_non_empty("Full name: ")
    student_class = get_non_empty("Class/Form: ")
    gender = get_non_empty("Gender: ")
    date_of_birth = get_date_of_birth()

    from student import Student
    student = Student(
        student_id,
        full_name,
        student_class,
        gender,
        date_of_birth,
    )
    students.append(student)
    save_students(students)
    print(f"Student {full_name} registered successfully.")


def view_all_students(students):
    print("\n--- REGISTERED STUDENTS ---")
    if not students:
        print("No students have been registered.")
        return

    print(f"{'ID':<14}{'FULL NAME':<28}{'CLASS':<18}{'SUBJECTS':>10}")
    print("-" * 70)
    for student in sorted(students, key=lambda item: item.full_name.lower()):
        print(
            f"{student.student_id:<14}"
            f"{student.full_name[:27]:<28}"
            f"{student.student_class[:17]:<18}"
            f"{len(student.scores):>10}"
        )
    print(f"\nTotal registered students: {len(students)}")


def search_student(students):
    print("\n--- SEARCH STUDENT ---")
    query = get_non_empty("Enter student ID or part of the name: ").lower()
    matches = [
        student for student in students
        if query in student.student_id.lower()
        or query in student.full_name.lower()
    ]

    if not matches:
        print("No matching student was found.")
        return

    for student in matches:
        print(build_student_report(student))


def update_student(students):
    print("\n--- UPDATE STUDENT INFORMATION ---")
    student = choose_student(students)
    if student is None:
        return

    print("Press Enter to keep the current value.")
    new_name = input(f"Full name [{student.full_name}]: ").strip()
    new_class = input(f"Class/Form [{student.student_class}]: ").strip()
    new_gender = input(f"Gender [{student.gender}]: ").strip()
    new_dob = input(
        f"Date of birth [{student.date_of_birth}] (YYYY-MM-DD): "
    ).strip()

    if new_dob:
        try:
            datetime.strptime(new_dob, "%Y-%m-%d")
        except ValueError:
            print("Invalid date. No changes were saved.")
            return

    if new_name:
        student.full_name = new_name
    if new_class:
        student.student_class = new_class
    if new_gender:
        student.gender = new_gender
    if new_dob:
        student.date_of_birth = new_dob

    save_students(students)
    print("Student information updated successfully.")


def delete_student(students):
    print("\n--- DELETE STUDENT ---")
    student = choose_student(students)
    if student is None:
        return

    confirmation = input(
        f"Delete {student.full_name} ({student.student_id})? Type YES to confirm: "
    ).strip()

    if confirmation == "YES":
        students.remove(student)
        save_students(students)
        print("Student record deleted.")
    else:
        print("Deletion cancelled.")


def enter_scores(students):
    print("\n--- ENTER STUDENT SCORES ---")
    student = choose_student(students)
    if student is None:
        return

    print("Enter at least five subjects. Type DONE when finished.")
    while True:
        subject = input("Subject name (or DONE): ").strip()
        if subject.upper() == "DONE":
            break
        if not subject:
            print("Subject name cannot be empty.")
            continue

        try:
            score = validate_score(input(f"{subject} score (0-100): "))
        except ValueError as error:
            print(error)
            continue

        student.add_score(subject, score)
        print(f"{subject.title()} score saved.")

    if len(student.scores) < MINIMUM_SUBJECTS:
        print(
            f"Note: {len(student.scores)} subject(s) recorded. "
            f"At least {MINIMUM_SUBJECTS} are needed for a final grade."
        )
    save_students(students)
    print("Student scores saved.")


def update_score(students):
    print("\n--- UPDATE EXISTING SCORE ---")
    student = choose_student(students)
    if student is None:
        return

    if not student.scores:
        print("This student has no recorded scores.")
        return

    print("Current scores:")
    for subject, score in student.scores.items():
        print(f"- {subject}: {float(score):.2f}")

    subject = get_non_empty("Enter the subject to update: ").title()
    if subject not in student.scores:
        print("That subject was not found.")
        return

    try:
        score = validate_score(input("Enter the new score (0-100): "))
    except ValueError as error:
        print(error)
        return

    student.add_score(subject, score)
    save_students(students)
    print("Score updated successfully.")


def display_report_card(students):
    print("\n--- INDIVIDUAL REPORT CARD ---")
    student = choose_student(students)
    if student:
        print(build_student_report(student))


def list_results(students):
    print("\n--- STUDENT RESULTS (HIGHEST AVERAGE FIRST) ---")
    if not students:
        print("No students are registered.")
        return

    ordered = sorted(
        students,
        key=lambda student: calculate_average(student.scores),
        reverse=True,
    )
    print(f"{'ID':<12}{'NAME':<25}{'TOTAL':>10}{'AVERAGE':>12}{'GRADE':>10}")
    print("-" * 69)

    for student in ordered:
        summary = result_summary(student.scores)
        print(
            f"{student.student_id:<12}"
            f"{student.full_name[:24]:<25}"
            f"{summary['total']:>10.2f}"
            f"{summary['average']:>12.2f}"
            f"{summary['grade']:>10}"
        )


def display_class_statistics(students):
    print("\n--- CLASS STATISTICS ---")
    stats = class_statistics(students)
    if not stats:
        print("No students have complete results yet.")
        return

    high_student, high_result = stats["highest"]
    low_student, low_result = stats["lowest"]

    print(f"Students with complete results: {stats['students_with_complete_results']}")
    print(
        f"Highest average: {high_result['average']:.2f} "
        f"- {high_student.full_name} ({high_student.student_id})"
    )
    print(
        f"Lowest average: {low_result['average']:.2f} "
        f"- {low_student.full_name} ({low_student.student_id})"
    )
    print(f"Class average: {stats['class_average']:.2f}")


def export_class_report(students):
    print("\n--- GENERATE CLASS REPORT ---")
    report = build_class_report(students)
    filename = f"class_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    report_path = __import__("pathlib").Path(__file__).resolve().parent / filename

    report_path.write_text(report, encoding="utf-8")
    print(report)
    print(f"\nReport saved to: {report_path.name}")


def show_menu():
    print("\n" + "=" * 48)
    print("       STUDENT RESULT MANAGEMENT SYSTEM")
    print("=" * 48)
    print("1.  Register new student")
    print("2.  View all students")
    print("3.  Search for student")
    print("4.  Update student information")
    print("5.  Delete student record")
    print("6.  Enter student scores")
    print("7.  Update existing scores")
    print("8.  View individual report card")
    print("9.  List all student results")
    print("10. Show class statistics")
    print("11. Generate and save class report")
    print("0.  Exit")
    print("-" * 48)


def main():
    try:
        students = load_students()
    except (RuntimeError, OSError) as error:
        print(f"Could not load student data: {error}")
        print("Please check data/students.json before continuing.")
        return

    print(f"Loaded {len(students)} student record(s).")

    actions = {
        "1": register_student,
        "2": view_all_students,
        "3": search_student,
        "4": update_student,
        "5": delete_student,
        "6": enter_scores,
        "7": update_score,
        "8": display_report_card,
        "9": list_results,
        "10": display_class_statistics,
        "11": export_class_report,
    }

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "0":
            save_students(students)
            print("Your records have been saved. Goodbye!")
            break

        action = actions.get(choice)
        if action is None:
            print("Invalid choice. Select an option from the menu.")
            continue

        try:
            action(students)
        except (OSError, RuntimeError) as error:
            print(f"An error occurred while working with files: {error}")


if __name__ == "__main__":
    main()
