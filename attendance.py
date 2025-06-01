import tkinter as tk
from tkinter import messagebox, ttk, Scrollbar
import mysql.connector
from datetime import date

def mark_attendance_ui(faculty_id):
    win = tk.Tk()
    win.title("Mark Attendance")
    win.geometry("600x600")
    win.resizable(False, False)

    conn = mysql.connector.connect(host="localhost", user="root", password="2004", database="lms")
    cursor = conn.cursor()

    course_id = faculty_id

    # Get all students (since every student studies every course)
    cursor.execute("SELECT id, name FROM students")
    students = cursor.fetchall()

    tk.Label(win, text=f"Mark Attendance for Course ID: {course_id}", font=("Arial", 16, "bold")).pack(pady=10)
    tk.Label(win, text="Mark each student as Present or Absent, then click Submit.", font=("Arial", 11)).pack(pady=5)

    # Frame for scrollable area
    frame = tk.Frame(win)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    canvas = tk.Canvas(frame, borderwidth=0, height=400)
    scroll_y = Scrollbar(frame, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas)

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scroll_y.set)

    canvas.pack(side="left", fill="both", expand=True)
    scroll_y.pack(side="right", fill="y")

    attendance_vars = {}
    attendance_var_refs = []

    tk.Label(scroll_frame, text="Student Name", font=("Arial", 12, "bold"), width=25, anchor="w").grid(row=0, column=0, padx=5, pady=5)
    tk.Label(scroll_frame, text="Present", font=("Arial", 12, "bold"), width=10, anchor="w").grid(row=0, column=1, padx=5, pady=5)
    tk.Label(scroll_frame, text="Absent", font=("Arial", 12, "bold"), width=10, anchor="w").grid(row=0, column=2, padx=5, pady=5)


    for idx, (sid, sname) in enumerate(students, start=1):
        var = tk.StringVar(master=scroll_frame, value="Absent")  # Default to Absent
        attendance_vars[sid] = var  # Store the variable FIRST
        
        tk.Label(scroll_frame, text=sname, font=("Arial", 11), width=25, anchor="w").grid(row=idx, column=0, padx=5, pady=3)

        rb_present = tk.Radiobutton(scroll_frame, text="Present", variable=var, value="Present", font=("Arial", 10), anchor="w")
        rb_present.grid(row=idx, column=1, padx=5, pady=3, sticky="w")

        rb_absent = tk.Radiobutton(scroll_frame, text="Absent", variable=var, value="Absent", font=("Arial", 10), anchor="w")
        rb_absent.grid(row=idx, column=2, padx=5, pady=3, sticky="w")
        
        
    def submit_attendance():
        today_date = date.today()
        try:
            for sid, var in attendance_vars.items():
                print(f"Student {sid}: {var.get()}")  # Debug: Should print "Present" or "Absent"
                cursor.execute(
                    "INSERT INTO attendance (course_id, student_id, date, status) VALUES (%s, %s, %s, %s)",
                    (course_id, sid, today_date, var.get())
                )
            conn.commit()
            messagebox.showinfo("Success", "Attendance submitted successfully!")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to submit attendance:\n{e}")

    tk.Button(win, text="Submit Attendance", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", command=submit_attendance).pack(pady=20)

    win.mainloop()
    cursor.close()
    conn.close()