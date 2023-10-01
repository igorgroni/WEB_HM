from sqlalchemy import func, desc, select

from connect_db import session
from models import Student, Group, Teacher, Lesson, Grade


def query_1():
    query = (
        session.query(
            Student.name, func.round(func.avg(Grade.rating)).label("avg_Rate")
        )
        .join(Grade, Student.StudentID == Grade.StudentID)
        .group_by(Student.StudentID)
        .order_by(func.round(func.avg(Grade.Rate)).desc())
        .limit(5)
        .all()
    )

    for student_name, avg_Rate in query:
        print(f"Student: {student_name}, Average Grade: {avg_Rate}")


def query_2():
    query = (
        session.query(Student.name, func.round(func.avg(Grade.Rate)).label("avg_grade"))
        .join(Grade, Student.StudentID == Grade.StudentID)
        .filter(Grade.LessonID == 4)
        .group_by(Student.id)
        .order_by(func.round(func.avg(Grade.Rate)).desc())
        .limit(1)
        .first()
    )

    if query:
        student_name, avg_Rate = query
        print(
            f"Student with Highest Average Grade in Subject 4: {student_name}, Average Grade: {avg_Rate}"
        )
    else:
        print("No data found")


def query_3():
    query = (
        session.query(
            Student.GroupID,
            Grade.LessonID,
            func.round(func.avg(Grade.Rate)).label("avg_Rate"),
        )
        .join(Grade, Student.StudentID == Grade.StudentID)
        .filter(Grade.LessonID == 2)
        .group_by(Student.GroupID, Grade.LessonID)
        .all()
    )

    for GroupID, LessonID, avg_Rate in query:
        print(f"Group: {GroupID}, Subject: {LessonID}, Average Grade: {avg_Rate}")


def query_4():
    query = session.query(func.round(func.avg(Grade.Rate)).label("avg_Rate")).first()

    if query:
        avg_Rate = query[0]
        print(f"Average Grade: {avg_Rate}")
    else:
        print("No data found")


def query_5():
    query = (
        session.query(Teacher.Teacher_Name, Lesson.LessonName)
        .join(Lesson, Teacher.TeacherID == Lesson.LessonID)
        .all()
    )

    for teacher_name, subject_name in query:
        print(f"Teacher: {teacher_name}, Subject: {subject_name}")


def query_6(GroupID):
    query = session.query(Student.student_name).filter(Student.GroupID == GroupID).all()

    for student_name in query:
        print(f"Student: {student_name[0]}")


def query_7(GroupID, LessonID):
    query = (
        session.query(Student.student_name, Grade.Rate)
        .join(Grade, Student.StudentID == Grade.StudentID)
        .filter(Student.GroupID == GroupID, Grade.LessonID == LessonID)
        .all()
    )

    for student_name, Rate in query:
        print(f"Student: {student_name}, Grade: {Rate}")


def query_8():
    query = (
        session.query(
            Teacher.teacher_name, func.round(func.avg(Grade.Rate)).label("avg_Rate")
        )
        .join(Lesson, Teacher.TeacherID == Lesson.TeacherID)
        .join(Grade, Lesson.LessonID == Grade.LessonID)
        .group_by(Teacher.teacher_name)
        .all()
    )

    for teacher_name, avg_Rate in query:
        print(f"Teacher: {teacher_name}, Average Grade: {avg_Rate}")


def query_9(RateID):
    query = (
        session.query(Student.student_name, Lesson.LessonName)
        .join(Grade, Student.StudentID == Grade.StudentID)
        .join(Lesson, Grade.LessonID == Lesson.LessonID)
        .filter(Grade.RateID == RateID)
        .all()
    )

    for student_name, LessonName in query:
        print(f"Student: {student_name}, Subject: {LessonName}")


def query_10(StudentID, TeacherID):
    query = (
        session.query(Student.student_name, Teacher.teacher_name, Lesson.LessonName)
        .join(Grade, Student.StudentID == Grade.StudentID)
        .join(Lesson, Grade.LessonID == Lesson.LessonID)
        .join(Teacher, Lesson.TeacherID == Teacher.TeacherID)
        .filter(Student.StudentID == StudentID, Teacher.TeacherID == TeacherID)
        .all()
    )

    for student_name, teacher_name, LessonName in query:
        print(
            f"Student: {student_name}, Teacher: {teacher_name}, Subject: {LessonName}"
        )
