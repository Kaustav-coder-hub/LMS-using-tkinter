import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel, ttk
import mysql.connector
from db import get_connection  # Assuming db.py is in the same directory

# --- DB Connection ---
# def get_connection():
#     return mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="2004",
#         database="lms"
#     )

def admin_page(logout_callback):
    admin = tk.Tk()
    admin.title("Admin Dashboard")
    admin.geometry("500x500")

    global role_var, name_entry, email_entry, pass_entry

    role_var = tk.StringVar()
    tk.Label(admin, text="Add User", font=("Arial", 16)).pack(pady=10)

    frame = tk.Frame(admin)
    frame.pack(pady=5)

    tk.Label(frame, text="Role:").grid(row=0, column=0)
    tk.OptionMenu(frame, role_var, "Student", "Faculty").grid(row=0, column=1)

    tk.Label(frame, text="Name:").grid(row=1, column=0)
    name_entry = tk.Entry(frame)
    name_entry.grid(row=1, column=1)

    tk.Label(frame, text="Email:").grid(row=2, column=0)
    email_entry = tk.Entry(frame)
    email_entry.grid(row=2, column=1)

    tk.Label(frame, text="Password:").grid(row=3, column=0)
    pass_entry = tk.Entry(frame, show="*")
    pass_entry.grid(row=3, column=1)

    tk.Button(admin, text="Add User", command=add_user).pack(pady=10)
    tk.Button(admin, text="Update User", command=update_user).pack(pady=5)
    tk.Button(admin, text="Delete User", command=delete_user).pack(pady=5)
    tk.Button(admin, text="View All Users", command=view_all_users_chart).pack(pady=10)
    tk.Button(admin, text="Logout", command=lambda: [admin.destroy(), logout_callback()]).pack(pady=10)

    admin.mainloop()

# --- Add User Function ---
def add_user():
    role = role_var.get()
    name = name_entry.get()
    email = email_entry.get()
    password = pass_entry.get()

    if role not in ("Student", "Faculty"):
        messagebox.showerror("Error", "Select a valid role")
        return

    table = "students" if role == "Student" else "faculty"
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = f"INSERT INTO {table} (name, email, password) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, email, password))
        conn.commit()
        messagebox.showinfo("Success", f"{role} added successfully!")
        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

# --- Update User Function ---
def update_user():
    role = role_var.get()
    email = email_entry.get()
    new_name = name_entry.get()
    new_password = pass_entry.get()

    if role not in ("Student", "Faculty"):
        messagebox.showerror("Error", "Select a valid role")
        return

    table = "students" if role == "Student" else "faculty"
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = f"UPDATE {table} SET name=%s, password=%s WHERE email=%s"
        cursor.execute(query, (new_name, new_password, email))
        if cursor.rowcount == 0:
            messagebox.showwarning("Update", "No user found with this email.")
        else:
            conn.commit()
            messagebox.showinfo("Success", f"{role} updated successfully!")
        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

# --- Delete User Function ---
def delete_user():
    role = role_var.get()
    email = email_entry.get()

    if role not in ("Student", "Faculty"):
        messagebox.showerror("Error", "Select a valid role")
        return

    table = "students" if role == "Student" else "faculty"
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = f"DELETE FROM {table} WHERE email=%s"
        cursor.execute(query, (email,))
        if cursor.rowcount == 0:
            messagebox.showwarning("Delete", "No user found with this email.")
        else:
            conn.commit()
            messagebox.showinfo("Success", f"{role} deleted successfully!")
        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

# --- View All Users in a Chart/Table ---
def view_all_users_chart():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 'Student' as role, id, name, email FROM students UNION ALL SELECT 'Faculty', id, name, email FROM faculty")
        users = cursor.fetchall()
        cursor.close()
        conn.close()

        chart_win = Toplevel()
        chart_win.title("All Users Chart")
        chart_win.geometry("600x400")

        cols = ("Role", "ID", "Name", "Email")
        tree = ttk.Treeview(chart_win, columns=cols, show="headings")
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=140)
        for row in users:
            tree.insert("", "end", values=row)
        tree.pack(expand=True, fill="both")

    except Exception as e:
        messagebox.showerror("Database Error", str(e))
