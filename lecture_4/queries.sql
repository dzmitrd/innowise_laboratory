-- find all grades for a specific student (Alice Johnson)
SELECT full_name, subject, grade FROM students 
    INNER JOIN grades ON students.id = grades.student_id
    WHERE students.full_name = 'Alice Johnson';

-- calculate the average grade per student
SELECT full_name, round(AVG(grade), 1) AS avg_grade FROM students 
    INNER JOIN grades ON students.id = grades.student_id
    GROUP BY full_name;

-- list all students born after 2004
SELECT full_name, birth_year FROM students 
    WHERE birth_year > 2004;

-- create a query that lists all subjects and their average grades
SELECT subject, round(AVG(grade), 1) AS avg_grade FROM grades 
    GROUP BY subject;

-- find the top 3 students with the highest average grades
SELECT full_name, round(AVG(grade), 1) as avg_grade FROM students 
    INNER JOIN grades ON students.id = grades.student_id
    GROUP BY full_name
    ORDER BY avg_grade DESC
    LIMIT 3;

-- show all students who have scored below 80 in any subject
SELECT full_name, subject, grade FROM students 
    INNER JOIN grades ON students.id = grades.student_id
    WHERE grade < 80;

