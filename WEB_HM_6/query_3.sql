SELECT GroupID, LessonID, (ROUND(AVG(grade))) AS avg_Rate
FROM students
JOIN rating ON Student_ID = rating.StudentID
WHERE rating.LessonID = 2
GROUP BY students.GroupID, rating.LessonID;