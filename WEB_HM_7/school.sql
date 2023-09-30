-- Table: students
DROP TABLE IF EXISTS students;
CREATE TABLE students (
    Student_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    GroupID INT,
    FOREIGN KEY (GroupID) REFERENCES groups(GroupID)
);

-- Table: groups
DROP TABLE IF EXISTS groups;
CREATE TABLE groups (
    GroupID INTEGER PRIMARY KEY AUTOINCREMENT,
    GroupName VARCHAR(50)
);

-- Table: teachers

DROP TABLE IF EXISTS teachers;
CREATE TABLE teachers (
    TeacherID INTEGER PRIMARY KEY AUTOINCREMENT,
    FirstName VARCHAR(50),
    LastName VARCHAR(50)
);

-- Table: lessons
DROP TABLE IF EXISTS lessons;
CREATE TABLE lessons (
    LessonID INTEGER PRIMARY KEY AUTOINCREMENT,
    LessonName VARCHAR(50),
    TeacherID INT,
    FOREIGN KEY (TeacherID) REFERENCES teachers (TeacherID)
);


-- Table: rating
DROP TABLE IF EXISTS rating;
CREATE TABLE rating (
    RateID INTEGER PRIMARY KEY AUTOINCREMENT,
    StudentID INT,
    LessonID INT,
    Rate INT,
    ExamDate DATE,
    FOREIGN KEY (StudentID) REFERENCES students(StudentID),
    FOREIGN KEY (LessonID) REFERENCES lessons(LessonID)
);
