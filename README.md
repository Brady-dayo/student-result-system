# Student Result Management System

A menu-driven Student Result Management System developed in Python for the New Horizon Introduction to Python Programming practical project.

## Features

### Student management
- Register students with ID, full name, class/form, gender and date of birth.
- View all registered students.
- Search by student ID or name.
- Update student information.
- Delete student records with confirmation.

### Score and result management
- Record scores for at least five subjects per student.
- Validate scores from 0 to 100.
- Update an existing subject score.
- Calculate total and average scores.
- Assign a grade when at least five subjects have been entered.
- Display an individual report card.

### Reporting and analysis
- List students ordered by average score (highest first).
- Display the highest average, lowest average and class average.
- Generate and save a text-based class report.

### Data persistence
- Save records in `data/students.json`.
- Load saved records when the application starts.
- Create the data folder/file as needed.

## Requirements

- Python 3.9 or later
- No third-party packages are required.

## How to run

1. Download or clone this repository.
2. Open the project folder in Visual Studio Code or a terminal.
3. Run:

```bash
python main.py
```

On some Windows installations, use:

```bash
py main.py
```

## Project structure

```text
student_result_system/
├── main.py
├── student.py
├── results.py
├── storage.py
├── reports.py
├── data/
│   └── students.json
└── README.md
```

## Grading scale

The project uses the following example grading scale:

| Average score | Grade |
|---:|:---:|
| 80–100 | A |
| 70–79.99 | B |
| 60–69.99 | C |
| 50–59.99 | D |
| 0–49.99 | F |

A final grade is shown only after at least five subject scores have been recorded. Scores are each out of 100.

## Python concepts demonstrated

- Variables, strings, numbers and type conversion
- Conditional statements and loops
- Lists and dictionaries
- Functions with parameters and return values
- Sorting with `sorted()` and `key`
- Exception handling with `try` and `except`
- JSON file reading and writing
- Modules and imports
- Object-oriented programming using the `Student` class
- Date and time handling with `datetime`
- Standard library modules including `json` and `pathlib`

## Data and privacy

Student records are stored locally in `data/students.json`. Use fictional student details when demonstrating the application. Do not upload real student personal information to a public repository.

## Notes

This is an educational command-line application. The grading bands are configurable in `results.py` to match an institution's official grading policy.
