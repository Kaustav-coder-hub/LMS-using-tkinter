import shutil
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta
import mysql.connector
import os
import webbrowser

def student_page(student_id, student_name, logout_callback):
    win = tk.Tk()
    win.title("Student Dashboard")
    win.geometry("450x500")
    tk.Label(win, text=f"Welcome {student_name}", font=("Arial", 14)).pack(pady=10)

    # View Course Content
    def view_course_content():
        """
        Displays a window listing all available course materials fetched from the database.

        Fetches course content information (title, file path, and upload date) from the 'course_content' table in the 'lms' MySQL database.
        Presents the content in a new Tkinter Toplevel window, allowing users to view and open each file.
        Handles file opening using the default web browser and displays error messages if files are missing or if a database error occurs.
        """
        # Placeholder: Replace with DB fetch logic
        messagebox.showinfo("Course Content", "Displaying course content.")
        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="2004", database="lms")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT cc.title, cc.file_path, cc.upload_date 
                FROM course_content cc
                INNER JOIN student_courses sc ON cc.course_id = sc.course_id
                WHERE sc.student_id = %s
            """, (student_id,))
            contents = cursor.fetchall()
            cursor.close()
            conn.close()

            viewer = tk.Toplevel()
            viewer.title("Course Content Viewer")
            viewer.geometry("600x400")

            tk.Label(viewer, text="Available Course Materials", font=("Arial", 14, "bold")).pack(pady=10)

            frame = tk.Frame(viewer)
            frame.pack(fill="both", expand=True)

            for i, (title, path, upload_date) in enumerate(contents, start=1):
                row = tk.Frame(frame)
                row.pack(fill="x", padx=10, pady=5)

                label = tk.Label(row, text=f"{i}. {title} ({upload_date})", anchor="w", width=50)
                label.pack(side="left")

                def open_file(p=path):
                    if os.path.exists(p):
                        webbrowser.open(p)
                    else:
                        messagebox.showerror("Error", f"File not found:\n{p}")

                btn = tk.Button(row, text="Open", command=open_file)
                btn.pack(side="right")

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    tk.Button(win, text="View Course Content", command=view_course_content).pack(pady=8)

    # Submit Assignments
    def submit_assignment(student_id):
        messagebox.showinfo("Submit Assignment", "Please Submit Assignment.")
        
        # New window for course selection
        course_win = tk.Toplevel()
        course_win.title("Submit Assignment")
        course_win.geometry("400x200")

        # Connect DB
        conn = mysql.connector.connect(host="localhost", user="root", password="2004", database="lms")
        cursor = conn.cursor()

        # Get available assignments
        cursor.execute("""
            SELECT a.id, c.course_name, a.course_id
            FROM assignments a
            JOIN courses c ON a.course_id = c.id
            WHERE a.deadline >= CURDATE()
        """)
        assignments = cursor.fetchall()
        conn.close()

        if not assignments:
            messagebox.showinfo("No Assignments", "No active assignments available.")
            course_win.destroy()
            return

        course_var = tk.StringVar()
        course_map = {}

        for aid, cname, cid in assignments:
            key = f"{cname} (Assignment ID: {aid})"
            course_map[key] = (aid, cid)

        tk.Label(course_win, text="Select Course:").pack(pady=10)
        tk.OptionMenu(course_win, course_var, *course_map.keys()).pack(pady=5)

        def proceed():
            selected = course_var.get()
            if not selected:
                messagebox.showerror("Error", "Please select a course.")
                return

            assignment_id, course_id = course_map[selected]
            file_path = filedialog.askopenfilename(title="Select Assignment File")
            if not file_path:
                return

            try:
                filename = os.path.basename(file_path)
                dest_folder = f"uploads/assignments/course_{course_id}/student_{student_id}"
                os.makedirs(dest_folder, exist_ok=True)
                dest_path = os.path.join(dest_folder, filename)
                shutil.copy(file_path, dest_path)

                # Insert into DB
                conn = mysql.connector.connect(host="localhost", user="root", password="2004", database="lms")
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO submissions (assignment_id, student_id, file_path)
                    VALUES (%s, %s, %s)
                """, (assignment_id, student_id, dest_path))
                conn.commit()
                cursor.close()
                conn.close()

                messagebox.showinfo("Success", f"Assignment submitted successfully:\n{filename}")
                course_win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Submission failed:\n{e}")

        tk.Button(course_win, text="Submit", command=proceed).pack(pady=10)
        
    tk.Button(win, text="Submit Assignment", command=lambda: submit_assignment(student_id)).pack(pady=8)

    # View Attendance
    def view_attendance(student_id):
        # Placeholder: Replace with DB fetch logic
        messagebox.showinfo("Attendance", "Displaying attendance records.")
        
        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="2004", database="lms")
            cursor = conn.cursor()

            # Get all course names and IDs
            cursor.execute("SELECT id, course_name FROM courses")
            courses = cursor.fetchall()
            course_map = {cid: cname for cid, cname in courses}
            course_names = [cname for _, cname in courses]

            # Get attendance records for past 5 weekdays
            start_date = (datetime.today() - timedelta(days=7)).date()

            cursor.execute("""
                SELECT 
                    a.course_id, 
                    DAYNAME(a.date) AS day_name, 
                    a.status
                FROM attendance a
                INNER JOIN student_courses sc ON a.course_id = sc.course_id
                WHERE sc.student_id = %s
                AND a.date >= %s
                AND DAYOFWEEK(a.date) BETWEEN 2 AND 6
            """, (student_id, start_date))

            records = cursor.fetchall()
            if not records:
                messagebox.showinfo("Attendance", "No attendance records found.")
                return

            # Structure: day -> course -> status
            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
            table = {day: {cname: "-" for cname in course_names} for day in days}

            for course_id, day_name, status in records:
                cname = course_map[course_id]
                if day_name in table:
                    table[day_name][cname] = "P" if status == "Present" else "A"

            # --- Add summary values for each day ---
            for day in days:
                row = table[day]
                total = len(course_names)
                present = sum(1 for c in course_names if row[c] == "P")
                row["Total"] = total
                row["Present"] = present
                row["Percentage"] = f"{(present / total * 100):.1f}%" if total else "0%"

            # --- Calculate weekly summary ---
            total_courses = len(course_names)
            total_days = len(days)
            total_possible = total_courses * total_days
            total_present = sum(
                1 for day in days for cname in course_names if table[day][cname] == "P"
            )
            total_percentage = (total_present / total_possible * 100) if total_possible else 0

            # --- Tkinter GUI ---
            view_win = tk.Toplevel()
            view_win.title("Attendance Report")
            view_win.geometry("1200x450")

            columns = ["Day"] + course_names + ["Total", "Present", "Percentage"]
            tree = ttk.Treeview(view_win, columns=columns, show="headings")

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=120, anchor="center")

            for day in days:
                row = [day] + [table[day][c] for c in course_names] + [
                    table[day]["Total"], table[day]["Present"], table[day]["Percentage"]
                ]
                tree.insert("", "end", values=row)

            tree.pack(fill="both", expand=True)

            xscroll = tk.Scrollbar(view_win, orient="horizontal", command=tree.xview)
            tree.configure(xscrollcommand=xscroll.set)
            xscroll.pack(side="bottom", fill="x")

            # --- Add summary labels below the table ---
            summary_frame = tk.Frame(view_win)
            summary_frame.pack(fill="x", pady=10)

            tk.Label(summary_frame, text=f"Total Courses in a Week: {total_courses}", font=("Arial", 12)).pack(side="left", padx=20)
            tk.Label(summary_frame, text=f"Total Days Present in a Week: {total_present}", font=("Arial", 12)).pack(side="left", padx=20)
            tk.Label(summary_frame, text=f"Total Percentage: {total_percentage:.1f}%", font=("Arial", 12)).pack(side="left", padx=20)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load attendance:\n{e}")
        

    tk.Button(win, text="View Attendance", command=lambda: view_attendance(student_id)).pack(pady=8)


    # View Marks and Feedback
    def view_marks_feedback(student_id):
        # Placeholder: Replace with DB fetch logic
        messagebox.showinfo("Marks & Feedback", "Displaying marks and feedback (demo).")
        
        win = tk.Toplevel()
        win.title("Marks & Feedback")
        win.geometry("900x400")

        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="2004", database="lms")
            cursor = conn.cursor()

            cursor.execute("""
                SELECT 
                    c.course_name,
                    a.description,
                    s.file_path,
                    COALESCE(s.marks, 'Not yet graded'),
                    COALESCE(s.feedback, 'No feedback')
                FROM submissions s
                JOIN assignments a ON s.assignment_id = a.id
                JOIN courses c ON a.course_id = c.id
                WHERE s.student_id = %s
            """, (student_id,))

            rows = cursor.fetchall()

            if not rows:
                messagebox.showinfo("Info", "No submissions found.")
                win.destroy()
                return

            columns = ["Course", "Assignment", "File", "Marks", "Feedback"]
            tree = ttk.Treeview(win, columns=columns, show="headings", height=12)

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, anchor="center", width=180)

            for row in rows:
                tree.insert("", "end", values=row)

            tree.pack(fill="both", expand=True, pady=10)
            cursor.close()
            conn.close()

        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            win.destroy()

    tk.Button(win, text="View Marks & Feedback", command=lambda: view_marks_feedback(student_id)).pack(pady=8)

    tk.Button(win, text="Logout", command=lambda: [win.destroy(), logout_callback()]).pack(pady=20)

    win.mainloop()
