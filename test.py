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