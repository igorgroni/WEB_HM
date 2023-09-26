SELECT FirstName || ' ' || LastName AS student_name, (ROUND(AVG(Rate))) as avg_Rate
FROM rating AS r
JOIN students AS s ON r.StudentID = s.Student_ID
WHERE LessonID = 4
GROUP BY StudentID
ORDER BY avg_Rate DESC
LIMIT 1;