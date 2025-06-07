# 📚 LMS App - Student Management System

A GUI-based LMS (Library Management System) built with **Python (Tkinter)** and **MariaDB**, ready to run using **Docker**.

---

## 🛠 Requirements

- [Docker Desktop](https://www.docker.com/products/docker-desktop) *(must be installed and running)*
- Python 3.x + pip *(only needed if running manually without Docker)*

---

## 📁 Project Structure

```
LMS-using-tkinter/
├── db/
│ └── lms_backup.sql # SQL dump of the LMS database
├── uploads/
│ └── assignments/
│   │ ├── course_2/
│   │ ├── course_3/
│   │ └── course_8/
│   ├── <uploded-files>
├── main.py 
├── admin_ui.py 
├── attendance.py 
├── db.py 
├── faculty_ui.py 
├── login.py 
├── session_utils.py 
├── student_ui.py 
├── session.txt 
├── docker-compose.yml # Starts MariaDB container
├── Dockerfile # For building the app into a container
├── requirements.txt # Python dependencies
└── README.md
```

---

## 🚀🚀 How to Run

### ✅ Step 1: Clone the Repository

```bash
git clone https://github.com/<your-username>/LMS-using-tkinter.git
cd LMS-using-tkinter
```

---


### ✅ Step 2: Start the MariaDB Server

```bash
docker compose up -d
```
This will:
- Start a MariaDB server on localhost:3307
- Load the lms database from db/lms_backup.sql
- Default credentials:
- Host: localhost
- Port: 3306
- User: root
- Password: 2004
- Database: lms


---


### ✅ Step 3: Run the App (on host)

Make sure you have Python installed, then create a virtual environment and install dependencies:

```bash
python -m venv venv
venv\Scripts\activate   # On Windows
# OR
source venv/bin/activate  # On Linux/macOS

pip install -r requirements.txt

```
Then run:
```
python main.py
```
This will:
- Start a MariaDB server on localhost:3307
- Load the lms database from db/lms_backup.sql
- Default credentials:
- Host: localhost
- Port: 3306
- User: root
- Password: 2004
- Database: lms


---


## 🧪 Testing DB Connection (Optional)

You can verify the MariaDB container is running:
```
docker exec -it <container_id_or_name> mysql -uroot -p2004
```

Inside the MySQL shell:
```
SHOW DATABASES;
USE lms;
SHOW TABLES;
```


---


## 📦 Deployment Strategy
To deploy on another machine:
1. Push this full project (excluding files ignored via .gitignore) to GitHub.
2. On another system:
   - Clone the repo.
   - Install DockerDesktop(Take help from [https://docs.docker.com/desktop/](https://docs.docker.com/desktop/) ).
   - Run docker compose up -d.
   - Optionally, set up Python and run python main.py.
  
The `lms_backup.sql` ensures your DB is always ready from the start.

## 📌 Notes
- Make sure Docker volumes or ports (3307) are not blocked by firewalls or other services.
- If you want a fully Dockerized GUI app (with X11 forwarding or VNC), extra steps are needed.

