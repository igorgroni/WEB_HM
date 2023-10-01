from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey, Table
from sqlalchemy.sql.sqltypes import DateTime


Base = declarative_base()


class Student(Base):
    __tablename__ = "students"
    StudentID = Column(Integer(), primary_key=True)
    FirstName = Column(String(250), nullable=False)
    LastName = Column(String(250), nullable=False)
    GroupID = Column(Integer(), ForeignKey("groups.GroupID", ondelete="CASCADE"))

    group = relationship("Group", back_populates="students")

    rating = relationship("Grade", back_populates="student")


class Group(Base):
    __tablename__ = "groups"
    GroupID = Column(Integer(), primary_key=True)
    GroupName = Column(String(250), nullable=False)

    students = relationship("Student", back_populates="group")


class Teacher(Base):
    __tablename__ = "teachers"
    TeacherID = Column(Integer(), primary_key=True)
    FirstName = Column(String(250), nullable=False)
    LastName = Column(String(250), nullable=False)

    lessons = relationship("Lesson", back_populates="teacher")


class Lesson(Base):
    __tablename__ = "lessons"
    LessonID = Column(Integer(), primary_key=True)
    LessonName = Column(String(250), nullable=False)
    TeacherID = Column(Integer(), ForeignKey("teachers.TeacherID", ondelete="CASCADE"))

    teacher = relationship("Teacher", back_populates="lessons")

    rating = relationship("Grade", back_populates="lesson")


class Grade(Base):
    __tablename__ = "rating"
    RateID = Column(Integer(), primary_key=True)
    StudentID = Column(Integer(), ForeignKey("students.StudentID", ondelete="CASCADE"))
    LessonID = Column(Integer(), ForeignKey("lessons.LessonID", ondelete="CASCADE"))
    Rate = Column(Integer())

    student = relationship("Student", back_populates="rating")
    lessons = relationship("Lesson", back_populates="rating")
