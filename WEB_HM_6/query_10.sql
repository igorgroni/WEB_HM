SELECT
    s.FirstName || ' ' || LastName AS student_name,
    t.FirstName || ' ' || LastName AS teacher_name,
    sb.LessonName
FROM rating g
JOIN students s ON g.StudentID = s.Student_ID
JOIN lessons sb ON g.StudentID = sb.RateID
JOIN teachers t ON sb.TeacherID = t.TeacherID
WHERE s.Student_ID = 28 AND t.TeacherID = 1;