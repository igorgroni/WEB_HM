from faker import Faker
import sqlite3
from datetime import datetime, timedelta
from random import randint, choice


NUMBER_STUDENTS = 35
NUMBER_GROUP = 3
NUMBER_TEACHERS = 5
lessons = ["Mathematics", "Literature", "History", "Geography", "Physics"]


def generate_fake_data(number_students, number_group, number_teachers) -> tuple():
    fake_students = []
    fake_group = []
    fake_teachers = []

    fake_data = Faker()

    for _ in range(number_students):
        fake_students.append(fake_data.name())

    for _ in range(number_group):
        fake_group.append(fake_data.word())

    for _ in range(number_teachers):
        fake_teachers.append(fake_data.name())

    return fake_students, fake_group, fake_teachers


def generate_grades(student_id, lesson_id):
    grades = []
    for _ in range(20):
        grade = randint(1, 10)  # Генеруємо випадкову оцінку від 1 до 10
        # Генеруємо випадкову дату від 18 до 25 років
        exam_date = datetime.now() - timedelta(days=randint(1, 365))
        grades.append((student_id, lesson_id, grade, exam_date))
    return grades


def prepare_data(conn, NUMBER_STUDENTS, NUMBER_TEACHERS, NUMBER_GROUP, lessons):
    cur = conn.cursor()

    students, groups, teachers = generate_fake_data(
        NUMBER_STUDENTS, NUMBER_GROUP, NUMBER_TEACHERS
    )

    # Додаємо студентів до таблиці students
    for student_name in students:
        cur.execute(
            "INSERT INTO students (FirstName, LastName, GroupID) VALUES (?, ?, ?)",
            (
                student_name.split()[0],
                student_name.split()[1],
                choice(range(1, NUMBER_GROUP + 1)),
            ),
        )

    # Додаємо групи до таблиці groups
    for group_name in groups:
        cur.execute("INSERT INTO groups (GroupName) VALUES (?)", (group_name,))

    # Додаємо викладачів до таблиці teachers
    for teacher_name in teachers:
        cur.execute(
            "INSERT INTO teachers (FirstName, LastName) VALUES (?, ?)",
            (teacher_name.split()[0], teacher_name.split()[1]),
        )

    # Додаємо уроки до таблиці lessons
    for lesson_name in lessons:
        cur.execute(
            "INSERT INTO lessons (LessonName, TeacherID) VALUES (?, ?)",
            (lesson_name, choice(range(1, NUMBER_TEACHERS + 1))),
        )

    # Додаємо оцінки для кожного студента та уроку
    for student_id in range(1, NUMBER_STUDENTS + 1):
        for lesson_id in range(1, len(lessons) + 1):
            grades = generate_grades(student_id, lesson_id)
            for grade in grades:
                cur.execute(
                    "INSERT INTO rating (StudentID, LessonID, Rate, ExamDate) VALUES (?, ?, ?, ?)",
                    (grade[0], grade[1], grade[2], grade[3]),
                )

    # Зберігаємо зміни у базі даних
    conn.commit()


if __name__ == "__main__":
    conn = sqlite3.connect("school.db")
    students, groups, teachers = generate_fake_data(
        NUMBER_STUDENTS, NUMBER_GROUP, NUMBER_TEACHERS
    )
    print(students)
    print(groups)
    print(teachers)
    prepare_data(conn, NUMBER_STUDENTS, NUMBER_TEACHERS, NUMBER_GROUP, lessons)
    conn.close()
