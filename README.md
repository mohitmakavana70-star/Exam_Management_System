# 🎓 Online Exam System

A secure online examination system built using **Python Flask**, **SQLite**, **HTML**, **CSS**, and **JavaScript**.

## 🚀 Features

### 👨‍🎓 Student Features
- User Signup
- Secure Login
- Attempt Exam Only Once
- Auto Score Calculation
- Auto Logout After Submission
- Mobile Responsive Interface

### 👨‍💼 Admin Features
- Admin Login
- Create New MCQ Exams
- Add Multiple Questions
- View Student Scores
- View Registered Users
- Delete Users
- Reset Exam Data

### 🔒 Anti-Cheating Features
- Detect Tab Switching
- Detect Page Visibility Change
- Detect Fullscreen Exit (Desktop)
- Detect Window Resize (Desktop)
- Disable Right Click
- Disable Copy/Cut
- Disable F12, Ctrl+Shift+I, Ctrl+Shift+J, Ctrl+U
- Automatic Exam Submission on Violation
- Student Blocked After Violation

---

## 🛠 Technologies Used

- Python
- Flask
- SQLite
- HTML5
- CSS3
- JavaScript

---

## 📂 Project Structure

```
project/
│
├── app.py
├── database.db
├── requirements.txt
├── Procfile
│
├── templates/
│   ├── login.html
│   ├── signup.html
│   ├── exam.html
│   ├── admin.html
│   ├── add_questions.html
│   ├── view_scores.html
│   └── blocked.html
│
└── static/
```

---

## ⚙ Installation

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/online-exam-system.git
```

### 2. Open Project

```bash
cd online-exam-system
```

### 3. Create Virtual Environment

```bash
python -m venv venv
```

### 4. Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### 5. Install Requirements

```bash
pip install -r requirements.txt
```

### 6. Run Application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

## 🌐 Deployment

This project can be deployed on:

- Render
- Railway
- PythonAnywhere

### Procfile

```text
web: gunicorn app:app
```

### requirements.txt

```text
Flask
gunicorn
Werkzeug
```

---

## 🔑 Admin Credentials

Default Admin Login:

```text
Username: admin
Password: admin@888
```

You can change these credentials in:

```python
if user == "admin" and pwd == "admin@888":
```

---

## 📊 Database Tables

### Users

| Field | Type |
|---------|---------|
| id | INTEGER |
| username | TEXT |
| password | TEXT |
| attempted | INTEGER |

### Questions

| Field | Type |
|---------|---------|
| id | INTEGER |
| question | TEXT |
| option_a | TEXT |
| option_b | TEXT |
| option_c | TEXT |
| option_d | TEXT |
| correct | TEXT |

### Scores

| Field | Type |
|---------|---------|
| id | INTEGER |
| username | TEXT |
| score | INTEGER |

---

## 🔐 Security Notes

This project provides basic browser-based anti-cheating measures.

However, no browser-only solution can completely prevent:
- External devices
- AI assistants on another phone
- Screenshots from another device
- Camera-based cheating

For high-stakes exams, use:
- Safe Exam Browser (SEB)
- Remote Proctoring
- Webcam Monitoring

---

## 👨‍💻 Author

Developed by **Mohit Makvana**

Full Stack Developer

- Python
- Flask
- React
- Node.js
- MongoDB

---

## 📜 License

This project is for educational purposes only.
