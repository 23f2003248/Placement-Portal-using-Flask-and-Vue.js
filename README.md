# Placement Portal

A full-stack placement management system built with **Flask** (backend) and **Vue.js** (frontend) for the App Dev II course project.

## Features

### Student
- Register and login
- Browse approved placement drives
- Apply to eligible drives (filtered by branch, year, CGPA)
- Track application status (`applied` → `shortlisted` → `interview_scheduled` → `selected` / `rejected`)
- Edit profile (name, email, branch, year, CGPA)
- Upload resume (PDF/DOC)
- Export application history as CSV (via email)

### Company
- Register and login (subject to admin approval)
- Create placement drives with eligibility criteria
- View applicants for each drive with full student details
- Shortlist, reject, or select applicants
- Schedule interviews with date/time picker

### Admin
- Approve or reject company registrations
- Approve or reject placement drives
- Blacklist / reactivate companies and students
- Search across students and companies
- View all records in one dashboard

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask, Flask-JWT-Extended, Flask-SQLAlchemy, Flask-Caching, Flask-Mail, Flask-CORS |
| Database | SQLite (via SQLAlchemy ORM) |
| Task Queue | Celery + Redis (falls back to sync if Redis unavailable) |
| Frontend | Vue.js 3 (Composition API), Vue Router, Axios |
| Styling | Bootstrap 5 |

---

## Project Structure

```
mad2_proj/
├── backend/
│   ├── app.py                  # Flask app factory & config
│   ├── models.py               # SQLAlchemy models (User, Student, Company, Drive, Application)
│   ├── celery_app.py           # Celery configuration & beat schedules
│   ├── tasks.py                # Background tasks (daily reminders, CSV export, monthly report)
│   ├── extensions.py           # Shared Flask extensions (cache, mail)
│   ├── routes/
│   │   ├── authorise.py        # POST /login
│   │   ├── student_route.py    # /student/*
│   │   ├── company_route.py    # /company/*
│   │   ├── drive_route.py      # /drive/*
│   │   ├── application_route.py# /application/*
│   │   └── admin_route.py      # /admin/*
│   └── static/
│       └── resumes/ 
|______ requirements.txt
           # Uploaded student resumes
├── frontend/
│   ├── src/
│   │   ├── router/
│   │   │   ├── index.js
│   │   │   └── views/
│   │   │       ├── LandingPage.vue
│   │   │       ├── Login.vue
│   │   │       ├── StudentRegister.vue
│   │   │       ├── StudentDashboard.vue
│   │   │       ├── CompanyRegister.vue
│   │   │       ├── CompanyDashboard.vue
│   │   │       ├── AdminDashboard.vue
│   │   │       └── CreateDrive.vue
│   │   ├── App.vue
│   │   └── main.js
│   └── package.json
└── README.md
```

---

## Setup & Running

### Prerequisites
- Python 3.10+
- Node.js 18+
- Redis *(optional — app falls back to in-memory cache if unavailable)*

### 1. Backend

```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Start the Flask server
cd backend
python app.py
```

The backend runs at **http://127.0.0.1:5000**

> A default admin account is created automatically on first run:
> - Email: `admin@admin.com`
> - Password: `admin123`

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend runs at **http://localhost:5173**

### 3. Celery Worker *(optional — for background tasks)*

```bash
# Requires Redis running on localhost:6379
cd backend
celery -A celery_app.celery worker --loglevel=info
celery -A celery_app.celery beat --loglevel=info
```

---

## API Overview

| Method | Endpoint | Description |
|---|---|---|
| POST | `/login` | Login for all roles |
| POST | `/student/register/` | Register a student |
| GET | `/student/all/` | List all students (public) |
| GET | `/student/<id>` | Get student by ID |
| PUT | `/student/update/<id>` | Update student profile |
| POST | `/student/upload_resume` | Upload resume file |
| POST | `/company/register/` | Register a company |
| GET | `/company/all/` | List all companies |
| GET | `/company/<id>/` | Get company by ID |
| POST | `/drive/register/` | Create a placement drive |
| GET | `/drive/all/` | Get all approved drives |
| GET | `/drive/all/admin/` | Get all drives (admin) |
| GET | `/drive/company/` | Get drives for logged-in company |
| POST | `/application/register` | Apply to a drive |
| GET | `/application/my/` | Get my applications (student) |
| GET | `/application/drive/<id>` | Get applicants for a drive (company) |
| PUT | `/application/update/<id>` | Update application status |
| POST | `/application/export/` | Export applications as CSV |
| PUT | `/admin/company/approve/<id>` | Approve/reject company |
| PUT | `/admin/drive/approve/<id>` | Approve/reject drive |
| PUT | `/admin/company/blacklist/<id>` | Blacklist/reactivate company |
| PUT | `/admin/student/blacklist/<id>` | Blacklist/reactivate student |
| GET | `/admin/search/?q=` | Search students & companies |

---

## Application Status Flow

```
applied → shortlisted → interview_scheduled → selected
                     ↘                      ↘ rejected
```

---

## Notes

- **Redis not required** — the app detects Redis at startup and falls back to simple in-memory caching automatically.
- **SMTP not required** — email tasks are wrapped in try/except and fail silently if an SMTP server is not configured.
- Student resumes are served statically from `backend/static/resumes/`.
