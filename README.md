# 🎓 AI Attendance System

An AI-powered classroom attendance management system that automates student attendance using **Face Recognition** and **Voice Recognition**.

The system provides separate interfaces for **students and teachers**, allowing student enrollment, subject management, AI-based attendance recording, and attendance analysis through an interactive Streamlit application.

---

## 🚀 Live Demo

### 👉 [Try the AI Attendance System](https://ai-attendance01.streamlit.app/)

> The application may take a few seconds to start if it has been inactive.

---

## 📌 Project Overview

Traditional classroom attendance requires teachers to manually call students or mark attendance one by one. This process can be time-consuming and can also lead to mistakes.

The **AI Attendance System** was developed to automate this process using artificial intelligence.

The application combines:

- 👤 Face Recognition
- 🎙️ Voice Recognition
- 🤖 Machine Learning
- 🗄️ Supabase Database
- 📊 Streamlit Web Interface
- 🔐 Authentication and Password Hashing

A teacher can create subjects, enroll students, and record attendance using either **face recognition** or **voice recognition**. Students can create their profiles, join subjects, and view their attendance records.

---

# ✨ Features

## 👨‍🎓 Student Features

- Student registration and login
- Face profile enrollment
- Voice profile enrollment
- View enrolled subjects
- Join subjects
- View attendance records
- View attendance percentage
- View attendance statistics

## 👨‍🏫 Teacher Features

- Teacher registration and login
- Create subjects
- Manage subjects
- Share subjects with students
- Enroll students into subjects
- View enrolled students
- Record attendance using Face Recognition
- Record attendance using Voice Recognition
- View classroom attendance records
- View student-wise attendance
- View attendance statistics
- View total classes conducted
- Prevent duplicate attendance records

---

# 🤖 AI Components

## 👤 Face Recognition

The face recognition system is used to identify students from their facial features.

The general pipeline is:

```text
Student Face
     ↓
Face Detection
     ↓
Face Encoding / Embedding
     ↓
Trained Classifier
     ↓
Student Identification
     ↓
Attendance Recording
```

During student enrollment, the system generates a facial representation for the student.

During attendance, the captured face is converted into an embedding and compared with the enrolled student profiles.

A trained machine-learning classifier is used for student identification.

---

## 🎙️ Voice Recognition

The system can also record classroom audio and identify students from their voices.

The general pipeline is:

```text
Classroom Audio
       ↓
Audio Processing
       ↓
Voice Embedding
       ↓
Comparison with Enrolled Profiles
       ↓
Student Identification
       ↓
Attendance Recording
```

Students create voice profiles during enrollment.

During attendance, classroom audio is processed and compared against the enrolled voice embeddings to determine which students are present.

---

# 🏗️ System Architecture

```text
                         ┌─────────────────────┐
                         │        User         │
                         │ Student / Teacher   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     Streamlit       │
                         │    Web Interface    │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
          ┌─────────────────┐             ┌─────────────────┐
          │ Face Recognition│             │ Voice Recognition│
          │     Pipeline    │             │     Pipeline     │
          └────────┬────────┘             └────────┬────────┘
                   │                               │
                   └───────────────┬───────────────┘
                                   │
                                   ▼
                         ┌─────────────────────┐
                         │ Attendance Matching │
                         │ & Processing        │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      Supabase       │
                         │      Database       │
                         └─────────────────────┘
```

---

# 🔄 Application Workflow

## 👨‍🏫 Teacher Workflow

```text
Teacher Registration / Login
             ↓
      Teacher Dashboard
             ↓
        Create Subject
             ↓
    Share / Manage Subject
             ↓
      Students Enroll
             ↓
      Record Attendance
             ↓
   ┌─────────┴─────────┐
   ↓                   ↓
Face Recognition   Voice Recognition
   ↓                   ↓
   └─────────┬─────────┘
             ↓
    Student Identification
             ↓
      Attendance Logs
             ↓
      Supabase Database
             ↓
    Attendance Dashboard
```

## 👨‍🎓 Student Workflow

```text
Student Registration
         ↓
      Login
         ↓
Create Face / Voice Profile
         ↓
    Join Subject
         ↓
   Attend Classroom
         ↓
    AI Identification
         ↓
 Attendance Recorded
         ↓
 View Attendance Statistics
```

---

# 🗄️ Database

The application uses **Supabase** as its backend database.

The database stores information related to:

- Students
- Teachers
- Subjects
- Subject enrollments
- Attendance logs
- Face profiles
- Voice profiles

The basic relationship can be represented as:

```text
Teacher
   │
   └── Subjects
          │
          └── Enrolled Students
                  │
                  └── Attendance Logs
```

---

# 🛡️ Duplicate Attendance Prevention

The system prevents a student from receiving multiple attendance records for the same subject on the same date.

The database uses a unique constraint based on:

```text
student_id + subject_id + attendance_date
```

This means that the same combination cannot be inserted more than once.

The application uses Supabase `upsert()` with the same conflict columns to handle duplicate attendance gracefully.

This provides duplicate protection at the **database level** while also allowing the application to handle duplicate insert attempts safely.

---

# 📊 Attendance Calculation

The teacher dashboard processes attendance records to calculate classroom attendance.

For each attendance session, the system calculates:

```text
Present Students / Total Students
```

For example:

```text
✅ 35 / 40 students
```

The application also determines the total number of classes using unique attendance dates.

Student attendance can then be represented using attendance statistics and percentages.

---

# 🛠️ Technology Stack

| Technology | Purpose |
|------------|---------|
| **Python** | Core programming language |
| **Streamlit** | Web application and user interface |
| **Supabase** | Backend database |
| **dlib** | Face detection and facial feature processing |
| **face_recognition** | Face encoding and recognition |
| **scikit-learn** | Machine learning classification |
| **NumPy** | Numerical operations |
| **Pandas** | Data processing and attendance analysis |
| **Librosa** | Audio processing |
| **Resemblyzer** | Voice embeddings |
| **bcrypt** | Password hashing |
| **Pillow** | Image processing |
| **Segno** | QR code generation |

---

# 🗂️ Project Structure

```text
AI-Attendance-System/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml
│
└── src/
    │
    └── screen/
        │
        ├── home_screen.py
        ├── student_screen.py
        ├── teacher_screen.py
        │
        ├── components/
        │   ├── header.py
        │   ├── share_subject_dialog.py
        │   └── ...
        │
        ├── database/
        │   ├── config.py
        │   └── db.py
        │
        ├── pipelines/
        │   ├── face_pipeline.py
        │   ├── voice_pipeline.py
        │   └── ...
        │
        └── ui/
            └── ...
```

---

# 🔐 Security

Sensitive credentials are not stored directly in the source code.

Supabase credentials are stored using Streamlit secrets.

The following file is intentionally excluded from GitHub:

```text
.streamlit/secrets.toml
```

The `.gitignore` configuration ensures that sensitive credentials are not accidentally committed.

> Never commit Supabase API keys, passwords, database credentials, or other private information to a public repository.

---

# 💻 Local Setup

## 1. Clone the Repository

```bash
git clone https://github.com/AKR-Anmol-Kumar-Rai/AI-Attendance-System.git
```

```bash
cd AI-Attendance-System
```

## 2. Create a Virtual Environment

For Windows:

```bash
python -m venv venv
```

Activate the virtual environment:

```bash
venv\Scripts\activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure Supabase

Create the following file:

```text
.streamlit/secrets.toml
```

Add your Supabase credentials:

```toml
SUPABASE_URL = "your-supabase-url"
SUPABASE_KEY = "your-supabase-key"
```

Use the exact variable names expected by the application's database configuration.

## 5. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

---

# ☁️ Deployment

The application is deployed using **Streamlit Community Cloud**.

### Deployment Configuration

```text
Repository:
AKR-Anmol-Kumar-Rai/AI-Attendance-System

Branch:
main

Entry Point:
app.py
```

### 🌐 Live Application

👉 **[Open the AI Attendance System](https://ai-attendance01.streamlit.app/)**

---

# 🎯 What This Project Demonstrates

This project demonstrates the integration of multiple areas of computer science and artificial intelligence into a complete working application.

### Artificial Intelligence

- Face recognition
- Voice recognition
- Face embeddings
- Voice embeddings
- Machine learning classification

### Software Development

- Python application development
- Streamlit UI development
- Modular project architecture
- Authentication
- Database integration
- Error handling

### Database

- Supabase
- Relational data
- Student-subject relationships
- Attendance logs
- Duplicate record prevention

### Deployment

- Git
- GitHub
- Streamlit Community Cloud
- Environment and secret management

---

# 🚧 Future Improvements

Some possible improvements for future versions include:

- 📱 Improved mobile responsiveness
- 📊 Advanced attendance analytics
- 📈 Interactive attendance charts
- 📧 Automated attendance notifications
- 📅 Calendar-based attendance reports
- 🎯 Improved face and voice recognition thresholds
- 🔊 Better performance in noisy classroom environments
- 📥 Export attendance reports to CSV/Excel
- 🏫 Multi-classroom support
- 🔐 More advanced authentication and role management

---

# 👨‍💻 Author

## Anmol Kumar Rai

Computer Science Engineering Student

### 🔗 Links

- 💻 **[GitHub Profile](https://github.com/AKR-Anmol-Kumar-Rai)**
- 🚀 **[Live Application](https://ai-attendance01.streamlit.app/)**

---

# ⭐ Support

If you find this project useful or interesting, consider giving the repository a ⭐ on GitHub.
