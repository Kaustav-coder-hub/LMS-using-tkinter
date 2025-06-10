import tkinter as tk
from tkinter import messagebox
from db import get_connection  # central DB connection
from admin_ui import admin_page
from student_ui import student_page
from faculty_ui import faculty_page
from login import login, show_login, logout_callback
from session_utils import save_session, clear_session, load_session

def ensure_database_tables_exist():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS faculty (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100) UNIQUE,
        password VARCHAR(100)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        id SERIAL PRIMARY KEY,
        course_name VARCHAR(100),
        faculty_id INTEGER,
        FOREIGN KEY (faculty_id) REFERENCES faculty(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100) UNIQUE,
        password VARCHAR(100)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS student_courses (
        id SERIAL PRIMARY KEY,
        student_id INTEGER NOT NULL,
        course_id INTEGER NOT NULL,
        FOREIGN KEY (student_id) REFERENCES students(id),
        FOREIGN KEY (course_id) REFERENCES courses(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assignments (
        id SERIAL PRIMARY KEY,
        course_id INTEGER,
        description TEXT,
        deadline DATE,
        FOREIGN KEY (course_id) REFERENCES courses(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS course_content (
        id SERIAL PRIMARY KEY,
        course_id INTEGER,
        title VARCHAR(255),
        file_path VARCHAR(255),
        upload_date DATE,
        FOREIGN KEY (course_id) REFERENCES courses(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS schedule (
        id SERIAL PRIMARY KEY,
        faculty_id INTEGER NOT NULL,
        day VARCHAR(20) NOT NULL,
        subject VARCHAR(100) NOT NULL,
        FOREIGN KEY (faculty_id) REFERENCES faculty(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS submissions (
        id SERIAL PRIMARY KEY,
        assignment_id INTEGER,
        student_id INTEGER,
        file_path VARCHAR(255),
        marks INTEGER,
        feedback TEXT,
        FOREIGN KEY (assignment_id) REFERENCES assignments(id),
        FOREIGN KEY (student_id) REFERENCES students(id)
    );
    """)

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
