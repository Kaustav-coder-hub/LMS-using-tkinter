import tkinter as tk

def test():
    win = tk.Tk()
    var = tk.StringVar(value="Present")
    tk.Radiobutton(win, text="Present", variable=var, value="Present").pack()
    tk.Radiobutton(win, text="Absent", variable=var, value="Absent").pack()
    def show():
        print(var.get())
    tk.Button(win, text="Submit", command=show).pack()
    win.mainloop()

test()

# INSERT INTO attendance (course_id, student_id, date, status) VALUES
# (1, 1, '2025-06-02', 'Absent'),
# (1, 2, '2025-06-02', 'Absent'),
# (1, 3, '2025-06-02', 'Present'),
# (1, 4, '2025-06-02', 'Absent'),
# (1, 5, '2025-06-02', 'Present'),
# (1, 7, '2025-06-02', 'Absent'),
# (1, 8, '2025-06-02', 'Absent'),
# (1, 9, '2025-06-02', 'Present'),
# (1, 10, '2025-06-02', 'Present'),
# (1, 11, '2025-06-02', 'Present'),
# (1, 12, '2025-06-02', 'Present'),
# (1, 13, '2025-06-02', 'Absent'),
# (1, 14, '2025-06-02', 'Absent'),
# (1, 15, '2025-06-02', 'Present'),
# (1, 16, '2025-06-02', 'Absent'),
# (1, 17, '2025-06-02', 'Absent'),
# (1, 18, '2025-06-02', 'Absent'),
# (1, 19, '2025-06-02', 'Present'),
# (1, 20, '2025-06-02', 'Present'),
# (1, 21, '2025-06-02', 'Present'),
# (1, 22, '2025-06-02', 'Absent'),
# (1, 23, '2025-06-02', 'Present'),
# (1, 24, '2025-06-02', 'Present'),
# (1, 25, '2025-06-02', 'Present'),
# (1, 26, '2025-06-02', 'Present'),
# (1, 27, '2025-06-02', 'Present'),
# (1, 28, '2025-06-02', 'Absent'),
# (1, 29, '2025-06-02', 'Absent'),
# (1, 30, '2025-06-02', 'Present'),
# (1, 31, '2025-06-02', 'Absent'),
# (1, 32, '2025-06-02', 'Present'),
# (1, 33, '2025-06-02', 'Present'),
# (1, 34, '2025-06-02', 'Present'),
# (1, 35, '2025-06-02', 'Absent'),
# (1, 36, '2025-06-02', 'Absent'),
# (1, 37, '2025-06-02', 'Absent'),
# (1, 38, '2025-06-02', 'Absent'),
# (1, 39, '2025-06-02', 'Present'),
# (1, 40, '2025-06-02', 'Present'),
# (1, 41, '2025-06-02', 'Absent'),
# (1, 42, '2025-06-02', 'Present'),
# (1, 43, '2025-06-02', 'Present'),
# (1, 44, '2025-06-02', 'Present'),
# (1, 45, '2025-06-02', 'Absent'),
# (1, 46, '2025-06-02', 'Present'),
# (1, 47, '2025-06-02', 'Present'),
# (1, 48, '2025-06-02', 'Present'),
# (1, 49, '2025-06-02', 'Present'),
# (1, 50, '2025-06-02', 'Present'),
# (1, 51, '2025-06-02', 'Present'),
# (1, 52, '2025-06-02', 'Absent'),
# (1, 53, '2025-06-02', 'Present'),
# (1, 54, '2025-06-02', 'Present'),
# (1, 55, '2025-06-02', 'Present');