SELECT student_name, (ROUND(AVG(Rate))) as avg_Rate
FROM rating
JOIN students ON rating.student_id = students.StudentID
WHERE LessonID = 4
GROUP BY student_id
ORDER BY avg_Rate DESC
LIMIT 1;