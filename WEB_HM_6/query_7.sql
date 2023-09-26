SELECT FirstName || ' ' || LastName AS student_name, Rate
FROM students
JOIN rating ON students.Student_ID = rating.StudentID
WHERE students.GroupID = 2 AND rating.LessonID = 3;