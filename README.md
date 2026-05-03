# 🚀 ClubHub – College Club Management System

A full-stack, role-based web application to manage college clubs, streamline event organization, and simplify student participation through a unified platform.

---

## 📌 Overview

ClubHub addresses the common problem of **fragmented club management in colleges**, where events and communications are scattered across multiple platforms.

This system provides a centralized solution where:

* Students can discover and register for events
* Club leaders can manage events and participants
* Admins can oversee the entire ecosystem

The platform ensures **structured workflows, secure access, and improved coordination** across all roles.

---

## ✨ Features

### 👤 Students

* Browse clubs and upcoming events
* One-click event registration
* Real-time event countdown timers
* View event details and galleries

### 👑 Club Leaders

* Create, update, and delete events
* Manage registrations (approve/reject)
* Upload post-event galleries
* Broadcast announcements
* Customize club profiles

### 🛡️ Admin

* Full control over users, clubs, and events
* Monitor platform activity and maintain system integrity

---

## 📸 Screenshots

> ⚠️ Add your actual screenshots here (very important for recruiters)
![Home](<Screenshot 2026-05-03 135747.png>)
* Student Dashboard
![DAshboard](<Screenshot 2026-05-03 140115.png>)
* Leader Dashboard
![Dashboard](<Screenshot 2026-05-03 140220.png>)
* Admin Dashboard
![Dashboard](<Screenshot 2026-05-03 141432.png>)


---

## ⚙️ Setup

### 1. Clone Repository

git clone https://github.com/your-username/clubhub-college-management-system.git
cd clubhub-college-management-system

### 2. Backend Setup

cd backend
pip install -r ../requirements.txt

### 3. Environment Configuration

Create a `.env` file inside `backend/`:

```env
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
SMTP_USERNAME=your_email
SMTP_PASSWORD=your_app_password
```

### 4. Initialize Database

python reset_db.py

### 5. Run Backend

uvicorn app.main:app --reload --port 8000

### 6. Run Frontend

cd frontend
python -m http.server 8080

### 7. Access Application

http://localhost:8080/index.html


## 🛠️ Tech Stack

### Frontend

* HTML5, CSS3, JavaScript
* Flexbox, CSS Grid
* Glassmorphism UI

### Backend

* Python 3.10+
* FastAPI
* SQLAlchemy, Pydantic
* JWT Authentication

### Database

* PostgreSQL (via Supabase)
