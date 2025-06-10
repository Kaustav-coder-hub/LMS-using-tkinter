import subprocess
import sys
import tkinter as tk
import os
import shutil
from tkinter import filedialog, messagebox
from datetime import date
from tkinter import ttk
from attendance import mark_attendance_ui
import psycopg2  # replace mysql.connector
from db import get_connection

def faculty_page(faculty_id, faculty_name, logout_callback):
    win = tk.Tk()
    win.title("Faculty Dashboard")
    win.geometry("400x400")
    tk.Label(win, text=f"Welcome {faculty_name}", font=("Arial", 14)).pack(pady=10)

    # Upload Course Content
    def upload_content():
        file_path = filedialog.askopenfilename(title="Select Course Content")
        if file_path:
            title = os.path.basename(file_path)
            upload_date = date.today()
            upload_dir = "uploads"  # central upload folder

            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)

            dest_path = os.path.join(upload_dir, title)

            try:
                shutil.copy(file_path, dest_path)  # copy to central folder

                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO course_content (course_id, title, file_path, upload_date) VALUES (%s, %s, %s, %s)",
                    (faculty_id, title, dest_path, upload_date)
                )
                conn.commit()
                cursor.close()
                conn.close()

                messagebox.showinfo("Upload", f"Uploaded to server: {title}")
            except Exception as e:
                messagebox.showerror("Error", f"Upload failed: {e}")

    tk.Button(win, text="Upload Course Content", command=upload_content).pack(pady=10)

    # Mark Attendance
    def mark_attendance():
        # Placeholder for attendance marking logic
        messagebox.showinfo("Attendance", "Give the ATTENDANCES of Students please!")
        mark_attendance_ui(faculty_id)
    # Replace with actual course ID from session or DB
    tk.Button(win, text="Mark Attendance", command=mark_attendance).pack(pady=10)

    # Evaluate Assignments
    def evaluate_assignments(faculty_id):
        # Placeholder for evaluation logic
        messagebox.showinfo("Evaluate", "Evaluate Assignment  !")
        
        win = tk.Toplevel()
        win.title("Evaluate Assignments")
        win.geometry("900x500")

        conn = get_connection()
        cursor = conn.cursor()

        # Step 1: Get the faculty's course_id
        cursor.execute("SELECT id FROM courses WHERE faculty_id = %s", (faculty_id,))
        course = cursor.fetchone()
        if not course:
            messagebox.showerror("Error", "No course found for this faculty.")
            win.destroy()
            return
        course_id = course[0]

        # Step 2: Get submissions for that course with marks IS NULL
        cursor.execute("""
            SELECT 
                s.id, st.name, a.description, s.file_path
            FROM submissions s
            JOIN assignments a ON s.assignment_id = a.id
            JOIN students st ON s.student_id = st.id
            WHERE a.course_id = %s AND s.marks IS NULL
        """, (course_id,))
        records = cursor.fetchall()

        if not records:
            messagebox.showinfo("Info", "No pending submissions to evaluate.")
            win.destroy()
            return

        selected_submission_id = tk.IntVar()
        marks_entry = tk.StringVar()
        feedback_entry = tk.StringVar()

        def submit_evaluation():
            sid = selected_submission_id.get()
            marks = marks_entry.get()
            feedback = feedback_entry.get()

            if not sid or not marks.isdigit():
                messagebox.showerror("Input Error", "Please select a submission and enter valid marks.")
                return

            try:
                cursor.execute("""
                    UPDATE submissions SET marks = %s, feedback = %s WHERE id = %s
                """, (int(marks), feedback, sid))
                conn.commit()
                messagebox.showinfo("Success", "Evaluation submitted successfully.")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update evaluation:\n{e}")

        # Table to display submissions
        columns = ("Student Name", "Assignment", "File")

        tree_frame = tk.Frame(win)
        tree_frame.pack(pady=10, fill="both", expand=True)

        h_scrollbar = tk.Scrollbar(tree_frame, orient="horizontal")
        h_scrollbar.pack(side="bottom", fill="x")

        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", xscrollcommand=h_scrollbar.set)
        h_scrollbar.config(command=tree.xview)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=200)

        # Store mapping from tree item to submission id
        item_to_id = {}

        for row in records:
            submission_id, student_name, assignment, file_path = row
            item = tree.insert("", "end", values=(student_name, assignment, file_path))
            item_to_id[item] = submission_id

        def on_select(event):
            selected = tree.focus()
            if selected:
                sid = item_to_id.get(selected)
                if sid:
                    selected_submission_id.set(sid)

        tree.bind("<<TreeviewSelect>>", on_select)
        tree.pack(side="top", fill="both", expand=True)

        def open_file():
            selected = tree.focus()
            if selected:
                file_path = tree.item(selected, 'values')[2]
                try:
                    if sys.platform.startswith('darwin'):
                        subprocess.call(['open', file_path])  # macOS
                    elif os.name == 'nt':
                        os.startfile(file_path)  # Windows
                    elif os.name == 'posix':
                        subprocess.call(['xdg-open', file_path])  # Linux
                    else:
                        messagebox.showerror("Unsupported OS", "Cannot determine how to open files on this OS.")
                except Exception as e:
                    messagebox.showerror("Error", f"Could not open file:\n{e}")
            else:
                messagebox.showwarning("No Selection", "Please select a file first.")

        tk.Button(win, text="Open Selected File", command=open_file, bg="#2196F3", fg="white").pack(pady=5)

        form = tk.Frame(win)
        form.pack(pady=10)

        tk.Label(form, text="Marks:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(form, textvariable=marks_entry).grid(row=0, column=1, padx=5)

        tk.Label(form, text="Feedback:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(form, textvariable=feedback_entry, width=40).grid(row=1, column=1, padx=5)

        tk.Button(form, text="Submit Evaluation", command=submit_evaluation, bg="#4CAF50", fg="white").grid(row=2, columnspan=2, pady=10)

        win.mainloop()
        cursor.close()
        conn.close()
        

    tk.Button(win, text="Evaluate Assignments", command=lambda: evaluate_assignments(faculty_id)).pack(pady=10)

    tk.Button(win, text="Logout", command=lambda: [win.destroy(), logout_callback()]).pack(pady=20)

    win.mainloop()