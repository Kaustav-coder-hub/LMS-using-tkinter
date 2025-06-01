import tkinter as tk
from tkinter import messagebox, filedialog
from attendance import mark_attendance_ui

def faculty_page(faculty_id, faculty_name, logout_callback):
    win = tk.Tk()
    win.title("Faculty Dashboard")
    win.geometry("400x400")
    tk.Label(win, text=f"Welcome {faculty_name}", font=("Arial", 14)).pack(pady=10)

    # Upload Course Content
    def upload_content():
        file_path = filedialog.askopenfilename(title="Select Course Content")
        if file_path:
            # Here you would save the file info to DB or copy to a directory
            messagebox.showinfo("Upload", f"Uploaded: {file_path}")

    tk.Button(win, text="Upload Course Content", command=upload_content).pack(pady=10)

    # Mark Attendance
    def mark_attendance():
        # Placeholder for attendance marking logic
        messagebox.showinfo("Attendance", "Give the ATTENDANCES of Students please!")
        mark_attendance_ui(faculty_id)
     # Replace with actual course ID from session or DB
    tk.Button(win, text="Mark Attendance", command=mark_attendance).pack(pady=10)

    # Evaluate Assignments
    def evaluate_assignments():
        # Placeholder for evaluation logic
        messagebox.showinfo("Evaluate", "Assignments evaluated (demo)!")

    tk.Button(win, text="Evaluate Assignments", command=evaluate_assignments).pack(pady=10)

    tk.Button(win, text="Logout", command=lambda: [win.destroy(), logout_callback()]).pack(pady=20)

    win.mainloop()