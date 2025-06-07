import tkinter as tk
from tkinter import messagebox
from db import get_connection  # central DB connection
from admin_ui import admin_page
from student_ui import student_page
from faculty_ui import faculty_page
from login import login, show_login, logout_callback
from session_utils import save_session, clear_session, load_session

def ensure_database_tables_exist():
    """Optional: create tables if they don't exist"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(""" CREATE DATABASE IF NOT EXISTS lms; """)
    cursor.execute(""" USE lms; """)
    cursor.execute(""" -- Table: faculty
CREATE TABLE IF NOT EXISTS faculty (
    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(100)
);""")
    
    cursor.execute(""" -- Table: courses
CREATE TABLE IF NOT EXISTS courses (
    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(100),
    faculty_id INT(11),
    FOREIGN KEY (faculty_id) REFERENCES faculty(id)
);""")
    
    cursor.execute(""" -- Table: students
CREATE TABLE IF NOT EXISTS students (
    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(100)
);""")
    
    cursor.execute(""" -- Table: student_courses
CREATE TABLE IF NOT EXISTS student_courses (
    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    student_id INT(11) NOT NULL,
    course_id INT(11) NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
);""")
    
    cursor.execute(""" -- Table: assignments
CREATE TABLE IF NOT EXISTS assignments (
    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    course_id INT(11),
    description TEXT,
    deadline DATE,
    FOREIGN KEY (course_id) REFERENCES courses(id)
);""")
    
    cursor.execute(""" -- Table: course_content
CREATE TABLE IF NOT EXISTS course_content (
    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    course_id INT(11),
    title VARCHAR(255),
    file_path VARCHAR(255),
    upload_date DATE,
    FOREIGN KEY (course_id) REFERENCES courses(id)
);""")
    
    cursor.execute(""" -- Table: schedule
CREATE TABLE IF NOT EXISTS schedule (
    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    faculty_id INT(11) NOT NULL,
    day VARCHAR(20) NOT NULL,
    subject VARCHAR(100) NOT NULL,
    FOREIGN KEY (faculty_id) REFERENCES faculty(id)
);""")
    
    cursor.execute(""" -- Table: submissions
CREATE TABLE IF NOT EXISTS submissions (
    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    assignment_id INT(11),
    student_id INT(11),
    file_path VARCHAR(255),
    marks INT(11),
    feedback TEXT,
    FOREIGN KEY (assignment_id) REFERENCES assignments(id),
    FOREIGN KEY (student_id) REFERENCES students(id)
);""")

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    ensure_database_tables_exist()  # makes the app Docker-ready

    role, user_id = load_session()

    if role == "Admin":
        admin_page(logout_callback)
    elif role == "Student" and user_id:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM students WHERE id=%s", (user_id,))
        result = cursor.fetchone()
        student_name = result[0] if result else ""
        cursor.close()
        conn.close()
        student_page(user_id, student_name, logout_callback)
    elif role == "Faculty" and user_id:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM faculty WHERE id=%s", (user_id,))
        result = cursor.fetchone()
        faculty_name = result[0] if result else ""
        cursor.close()
        conn.close()
        faculty_page(user_id, faculty_name, logout_callback)
    else:
        show_login()
