import tkinter as tk
from tkinter import messagebox
import mysql.connector
import os
from admin_ui import admin_page
from student_ui import student_page
from faculty_ui import faculty_page
from login import login, show_login, logout_callback
from session_utils import save_session, clear_session, load_session

if __name__ == "__main__":
    role, user_id = load_session()
   
    if role == "Admin":
        admin_page(logout_callback)
    elif role == "Student" and user_id:
        conn = mysql.connector.connect(host="localhost", user="root", password="2004", database="lms")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM students WHERE id=%s", (user_id,))
        result = cursor.fetchone()
        student_name = result[0] if result else ""
        cursor.close()
        conn.close()
        student_page(user_id, student_name, logout_callback)
    elif role == "Faculty" and user_id:
        # Fetch faculty_name from DB using user_id
        conn = mysql.connector.connect(host="localhost", user="root", password="2004", database="lms")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM faculty WHERE id=%s", (user_id,))
        result = cursor.fetchone()
        faculty_name = result[0] if result else ""
        cursor.close()
        conn.close()
        faculty_page(user_id, faculty_name, logout_callback)
    else:
        show_login()
