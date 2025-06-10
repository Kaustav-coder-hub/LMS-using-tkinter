-- Table structure for table "assignments"

DROP TABLE IF EXISTS assignments;
CREATE TABLE assignments (
  id SERIAL PRIMARY KEY,
  course_id INT REFERENCES courses(id) ON DELETE CASCADE,
  description TEXT DEFAULT NULL,
  deadline DATE DEFAULT NULL
);

-- Table structure for table "attendance"

DROP TABLE IF EXISTS attendance;
CREATE TABLE attendance (
    id SERIAL PRIMARY KEY,
    course_id INT REFERENCES courses(id) ON DELETE CASCADE,
    student_id INT REFERENCES students(id) ON DELETE CASCADE,
    date DATE,
    status TEXT CHECK (status IN ('Present', 'Absent'))
);

-- Table structure for table "course_content"

DROP TABLE IF EXISTS course_content;
CREATE TABLE course_content (
  id SERIAL PRIMARY KEY,
  course_id INT REFERENCES courses(id) ON DELETE CASCADE,
  title VARCHAR(255) DEFAULT NULL,
  file_path VARCHAR(255) DEFAULT NULL,
  upload_date DATE DEFAULT NULL
);

-- Table structure for table "courses"

DROP TABLE IF EXISTS courses;
CREATE TABLE courses (
  id SERIAL PRIMARY KEY,
  course_name VARCHAR(100) DEFAULT NULL,
  faculty_id INT REFERENCES faculty(id) ON DELETE SET NULL
);

-- Table structure for table "faculty"

DROP TABLE IF EXISTS faculty;
CREATE TABLE faculty (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) DEFAULT NULL,
  email VARCHAR(100) DEFAULT NULL UNIQUE,
  password VARCHAR(100) DEFAULT NULL
);

-- Table structure for table "student_courses"

DROP TABLE IF EXISTS student_courses;
CREATE TABLE student_courses (
  id SERIAL PRIMARY KEY,
  student_id INT REFERENCES students(id),
  course_id INT REFERENCES courses(id)
);

-- Table structure for table "students"

DROP TABLE IF EXISTS students;
CREATE TABLE students (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) DEFAULT NULL,
  email VARCHAR(100) DEFAULT NULL UNIQUE,
  password VARCHAR(100) DEFAULT NULL
);

-- Table structure for table "submissions"

DROP TABLE IF EXISTS submissions;
CREATE TABLE submissions (
  id SERIAL PRIMARY KEY,
  assignment_id INT REFERENCES assignments(id) ON DELETE CASCADE,
  student_id INT REFERENCES students(id) ON DELETE CASCADE,
  file_path VARCHAR(255) DEFAULT NULL,
  marks INT DEFAULT NULL,
  feedback TEXT DEFAULT NULL
);