# filepath: session_utils.py
import os

SESSION_FILE = "session.txt"

def save_session(role, user_name=None):
    with open(SESSION_FILE, "w") as f:
        f.write(f"{role},{user_name if user_name else ''}")

def clear_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)

def load_session():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE) as f:
            data = f.read().strip().split(",")
            if data[0] == "Admin":
                return ("Admin", None)
            elif data[0] in ("Student", "Faculty") and data[1]:
                return (data[0], data[1])
    return (None, None)