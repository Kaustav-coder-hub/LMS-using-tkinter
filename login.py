from admin_ui import admin_page
from student_ui import student_page
from faculty_ui import faculty_page
import tkinter as tk
from tkinter import messagebox
import mysql.connector
import os
import tkinter as tk
from tkinter import messagebox, filedialog
from session_utils import save_session, clear_session
 
    
def show_login():
    global app, email_entry, pass_entry, role_var
    app = tk.Tk()
    app.title("Login Page")
    app.geometry("450x500")

    role_var = tk.StringVar(value="Student")
    tk.Label(app, text="Role").pack()
    tk.OptionMenu(app, role_var, "Student", "Faculty", "Admin").pack()

    tk.Label(app, text="Email").pack()
    email_entry = tk.Entry(app)
    email_entry.pack()

    tk.Label(app, text="Password").pack()
    pass_entry = tk.Entry(app, show="*"
                          )
    pass_entry.pack()

    tk.Button(app, text="Login", command=login).pack()
    app.mainloop()

def login():
    email = email_entry.get()
    password = pass_entry.get()
    role = role_var.get()
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="2004",
        database="lms"
    )
    cursor = conn.cursor()

    if role == "Student":
        cursor.execute("SELECT id, name FROM students WHERE email=%s AND password=%s", (email, password))
        result = cursor.fetchone()
        if result:
            save_session("Student", result[0])
            messagebox.showinfo("Login", f"Welcome Student")
            app.destroy()
            student_page(result[0],result[1], logout_callback)
        else:
            messagebox.showerror("Error", "Invalid credentials")

    elif role == "Faculty":
        cursor.execute("SELECT id, name FROM faculty WHERE email=%s AND password=%s", (email, password))
        result = cursor.fetchone()
        if result:
            save_session("Faculty", result[0])
            messagebox.showinfo("Login", f"Welcome Faculty")
            app.destroy()
            faculty_page(result[0],result[1], logout_callback)
        else:
            messagebox.showerror("Error", "Invalid credentials")

    elif role == "Admin":
        if email == "admin" and password == "admin123":
            save_session("Admin")
            messagebox.showinfo("Login", "Welcome Admin")
            app.destroy()
            admin_page(logout_callback)
        else:
            messagebox.showerror("Error", "Invalid Admin Credentials")

def logout_callback():
    clear_session()
    show_login()
