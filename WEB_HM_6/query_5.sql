SELECT
    t.FirstName || ' ' || LastName,
    s.LessonName
FROM teachers t
JOIN lessons s ON t.TeacherID = s.LessonID;