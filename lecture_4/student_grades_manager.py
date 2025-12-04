import sqlite3 as sl

# data
students_dt = [
    ('Alice Johnson', 2005),
    ('Brian Smith', 2004),
    ('Carla Reyes', 2006),
    ('Daniel Kim', 2005),
    ('Eva Thompson', 2003),
    ('Felix Nguyen', 2007),
    ('Grace Patel', 2005),
    ('Henry Lopez', 2004),
    ('Isabella Martinez', 2006)
]

grades_dt = [
    (1, 'Math', 88),
    (1, 'English', 92),
    (1, 'Science', 85),
    (2, 'Math', 75),
    (2, 'History', 83),
    (2, 'English', 79),
    (3, 'Science', 95),
    (3, 'Math', 91),
    (3, 'Art', 89),
    (4, 'Math', 84),
    (4, 'Science', 88),
    (4, 'Physical Education', 93),
    (5, 'English', 90),
    (5, 'History', 85),
    (5, 'Math', 88),
    (6, 'Science', 72),
    (6, 'Math', 78),
    (6, 'English', 81),
    (7, 'Science', 87),
    (7, 'Math', 90),
    (8, 'History', 77),
    (8, 'Math', 83),
    (8, 'Science', 80),
    (9, 'English', 96),
    (9, 'Math', 89),
    (9, 'Art', 92)
]

# connection with db
con = sl.connect('school.db')
con.execute("PRAGMA foreign_keys = ON")
cursor = con.cursor()

# create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
id INTEGER PRIMARY KEY AUTOINCREMENT,
full_name TEXT NOT NULL,
birth_year INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    subject TEXT NOT NULL ,
    grade INTEGER NOT NULL CHECK(grade BETWEEN 1 AND 100),
    FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE
)
''')

# import data
cursor.execute("SELECT 1 FROM students LIMIT 1")
if cursor.fetchone() is None:
    with con:
        con.executemany('INSERT INTO students (full_name, birth_year) values(?, ?)', students_dt)

cursor.execute("SELECT 1 FROM grades LIMIT 1")
if cursor.fetchone() is None:
    with con:
        con.executemany('INSERT INTO grades (student_id, subject, grade) values(?, ?, ?)', grades_dt)

# indexes
cursor.execute('CREATE INDEX IF NOT EXISTS idx_students_full_name ON students(full_name)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_grades_student_id ON grades(student_id)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_grades_subject ON grades(subject)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_grades_grade ON grades(grade)')

# queries
query1_sql = ('-- find all grades for a specific student (Alice Johnson)', '''
    SELECT full_name, subject, grade FROM students 
    INNER JOIN grades ON students.id = grades.student_id
    WHERE students.full_name = 'Alice Johnson';
    ''')
query2_sql = ('-- calculate the average grade per student',
    '''
    SELECT full_name, round(AVG(grade), 1) AS avg_grade FROM students 
    INNER JOIN grades ON students.id = grades.student_id
    GROUP BY full_name;
    ''')
query3_sql = ('-- list all students born after 2004',
    '''
    SELECT full_name, birth_year FROM students 
    WHERE birth_year > 2004;
    ''')
query4_sql = ('-- create a query that lists all subjects and their average grades',
    '''
    SELECT subject, round(AVG(grade), 1) AS avg_grade FROM grades 
    GROUP BY subject;
    ''')
query5_sql = ('-- find the top 3 students with the highest average grades',
    '''
    SELECT full_name, round(AVG(grade), 1) as avg_grade FROM students 
    INNER JOIN grades ON students.id = grades.student_id
    GROUP BY full_name
    ORDER BY avg_grade DESC
    LIMIT 3;
    ''')
query6_sql = ('-- show all students who have scored below 80 in any subject',
    '''
    SELECT full_name, subject, grade FROM students 
    INNER JOIN grades ON students.id = grades.student_id
    WHERE grade < 80;
    ''')
queries_sql = (query1_sql, query2_sql, query3_sql, query4_sql, query5_sql, query6_sql)

def req_sql_and_write_file(connect, queries_list):
    with connect:
        with open("queries.sql", "w", encoding="utf-8") as file:
            for query in queries_list:
                connect.execute(query[1])
                file.write(query[0].strip() + "\n" + query[1].strip() + "\n\n")

'''
with con:
    # 1. find all grades for a specific student (Alice Johnson)
    query1 = con.execute(query1_sql[1])
    # 2. calculate the average grade per student
    query2 = con.execute(query2_sql[1])
    # 3. list all students born after 2004
    query3 = con.execute(query3_sql[1])
    # 4. create a query that lists all subjects and their average grades
    query4 = con.execute(query4_sql[1])
    # 5. find the top 3 students with the highest average grades
    query5 = con.execute(query5_sql[1])
    # 6. show all students who have scored below 80 in any subject
    query6 = con.execute(query6_sql[1])
    '''

req_sql_and_write_file(con, queries_sql)

con.close()
