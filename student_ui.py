import tkinter as tk
from tkinter import messagebox, filedialog

def student_page(student_id, student_name, logout_callback):
    win = tk.Tk()
    win.title("Student Dashboard")
    win.geometry("450x500")
    tk.Label(win, text=f"Welcome {student_name}", font=("Arial", 14)).pack(pady=10)

    # View Course Content
    def view_course_content():
        # Placeholder: Replace with DB fetch logic
        messagebox.showinfo("Course Content", "Displaying course content (demo).")

    tk.Button(win, text="View Course Content", command=view_course_content).pack(pady=8)

    # Submit Assignments
    def submit_assignment():
        file_path = filedialog.askopenfilename(title="Select Assignment to Submit")
        if file_path:
            # Placeholder: Save submission to DB or directory
            messagebox.showinfo("Submit Assignment", f"Assignment submitted: {file_path}")

    tk.Button(win, text="Submit Assignment", command=submit_assignment).pack(pady=8)

    # View Attendance
    def view_attendance():
        # Placeholder: Replace with DB fetch logic
        messagebox.showinfo("Attendance", "Displaying attendance records (demo).")

    tk.Button(win, text="View Attendance", command=view_attendance).pack(pady=8)


    # View Marks and Feedback
    def view_marks_feedback():
        # Placeholder: Replace with DB fetch logic
        messagebox.showinfo("Marks & Feedback", "Displaying marks and feedback (demo).")

    tk.Button(win, text="View Marks & Feedback", command=view_marks_feedback).pack(pady=8)

    tk.Button(win, text="Logout", command=lambda: [win.destroy(), logout_callback()]).pack(pady=20)

    win.mainloop()
