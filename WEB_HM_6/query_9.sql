SELECT FirstName || ' ' || LastName AS student_name, LessonName
FROM rating g
JOIN students st ON g.StudentID = st.Student_ID
JOIN subjects sb ON g.StudentID = sb.LessonID
WHERE g.RateID = 28;