# SmartHire Backend

REST API backend for SmartHire — an AI-powered job application tracker built with Django and PostgreSQL.

**Live API:** https://smart-hire-l974.onrender.com  
**Frontend:** https://smarthire01.vercel.app  
**Frontend Repo:** https://github.com/theAmrit07/smarthire-frontend

---

## What it does

SmartHire helps job seekers track their applications and get AI-powered feedback on how well their CV matches a job description. This repo contains the Django REST API backend.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | Django 6, Django REST Framework |
| Authentication | JWT (djangorestframework-simplejwt) |
| Database | PostgreSQL |
| AI Integration | Groq API (LLaMA 3.3-70b) |
| Deployment | Render |
| Environment | python-dotenv, dj-database-url |

---

## API Endpoints

### Authentication
```
POST /api/auth/register/     Create a new user account
POST /api/auth/login/        Login and receive JWT access + refresh tokens
POST /api/auth/refresh/      Refresh an expired access token
```

### Job Applications
```
GET    /api/applications/              List all applications for logged-in user
POST   /api/applications/             Create a new job application
GET    /api/applications/:id/         Get a single application
PUT    /api/applications/:id/         Update an application
DELETE /api/applications/:id/         Delete an application
POST   /api/applications/:id/analyze/ Run AI analysis on CV vs job description
```

### Dashboard
```
GET /api/dashboard/stats/    Get application counts by status
```

---

## AI Analysis

The `/analyze/` endpoint accepts a CV text and compares it against the job description stored for that application using Groq's LLaMA 3.3-70b model. It returns:

- Match score (0–100)
- Key strengths
- Gaps
- Improvement suggestions

---

## Running Locally

### Prerequisites
- Python 3.11+
- PostgreSQL

### Setup

```bash
# Clone the repo
git clone https://github.com/theAmrit07/Smart-Hire.git
cd Smart-Hire

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Fill in your values (see Environment Variables below)

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

### Environment Variables

Create a `.env` file in the root directory:

```
SECRET_KEY=your-django-secret-key
DEBUG=True
DB_NAME=smarthire
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432
GROQ_API_KEY=your-groq-api-key
```

Get a free Groq API key at https://console.groq.com

---

## Project Structure

```
smarthire/
├── smarthire/          # Project config (settings, urls, wsgi)
├── jobs/               # Main app
│   ├── models.py       # JobApplication model
│   ├── serializers.py  # DRF serializers
│   ├── views.py        # API views and AI integration
│   └── urls.py         # App URL routing
├── requirements.txt
├── Procfile            # Render deployment
└── manage.py
```

---

## Deployment

The backend is deployed on **Render** with a PostgreSQL database.

On every deploy, migrations run automatically via the start command:
```
bash -c "python manage.py migrate && gunicorn smarthire.wsgi"
```

---

## Author

**Amrit Chataut**  
[LinkedIn](https://linkedin.com/in/amrit-chataut-426949246) · [GitHub](https://github.com/theAmrit07)