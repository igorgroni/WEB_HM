SELECT FirstName || ' ' || LastName AS teacher_name, (ROUND(AVG(g.Rate))) AS avg_Rate
FROM teachers t
JOIN lessons sb ON t.TeacherID = sb.TeacherID
JOIN rating g ON sb.LessonID = g.LessonID
GROUP BY t.teacher_name;