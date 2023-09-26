SELECT FirstName || ' ' || LastName AS student_name, ROUND(AVG(r.Rate)) AS avg_Rate
FROM students AS s
JOIN rating AS r ON s.Student_ID = r.StudentID 
GROUP BY student_name
ORDER BY avg_Rate DESC
LIMIT 5;


