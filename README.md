# 🏥 Healthcare Backend API

A production-ready RESTful backend for a healthcare management system built with **Django**, **Django REST Framework**, and **PostgreSQL**.  
Users can register, authenticate via JWT, and manage **patient records**, **doctor profiles**, and **patient–doctor assignments** through a clean API.

---

## ✨ Features

| Area | Details |
|------|---------|
| **Authentication** | JWT-based auth via `djangorestframework-simplejwt` — tokens issued on both registration and login |
| **Patient Management** | Full CRUD, ownership-scoped (users only see their own patients) |
| **Doctor Management** | Full CRUD for doctor profiles with email uniqueness |
| **Patient–Doctor Mapping** | Assign / unassign doctors to patients with duplicate prevention (`unique_together`) |
| **Security** | Environment-variable config, ownership isolation, password validation |
| **API Documentation** | Interactive Swagger UI at `/api/docs/` with OpenAPI 3.0 schema via `drf-spectacular` |
| **Code Quality** | Formatted with Black + isort, linted with flake8, 31 automated tests |

---

## 🗂️ Project Structure

```
healthcare-backend/
├── core/                   # Django project configuration
│   ├── settings.py         # DRF · JWT · PostgreSQL · CORS
│   ├── urls.py             # Root URL router
│   └── wsgi.py
├── accounts/               # User registration & login
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
├── patients/               # Patient CRUD (ownership-scoped)
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
├── doctors/                # Doctor CRUD
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
├── mappings/               # Patient ↔ Doctor assignments
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── requirements.txt
├── setup.cfg               # flake8 + isort config
├── pyproject.toml           # black config
├── .env.example
└── manage.py
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 14+ (or Docker Desktop)

### Option A — Docker (recommended)

```bash
cp .env.example .env          # configure your secrets
docker compose up -d --build  # starts PostgreSQL + Django
```

The API will be available at **http://localhost:8000**.  
Swagger docs → **http://localhost:8000/api/docs/**

### Option B — Local setup

```bash
# 1. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate      # macOS / Linux
# venv\Scripts\activate       # Windows

# 2. Install dependencies
make install
# or: pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your PostgreSQL credentials

# 4. Run migrations
make migrate
# or: python manage.py migrate

# 5. Start the server
make run
# or: python manage.py runserver
```

> 💡 Once the server is running, visit **http://localhost:8000** — it redirects straight to the interactive Swagger UI where you can explore and test every endpoint.

---

## 📡 API Reference

> **Interactive docs:** [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/) (Swagger UI)  
> **OpenAPI schema:** [http://localhost:8000/api/schema/](http://localhost:8000/api/schema/) (YAML)

### Authentication

| Method | Endpoint | Auth | Body | Description |
|--------|----------|:----:|------|-------------|
| `POST` | `/api/auth/register/` | ❌ | `name`, `email`, `password` | Register and receive JWT tokens |
| `POST` | `/api/auth/login/` | ❌ | `username`, `password` | Login and receive JWT tokens |
| `POST` | `/api/auth/token/refresh/` | ❌ | `refresh` | Refresh an expired access token |

### Patients

| Method | Endpoint | Auth | Description |
|--------|----------|:----:|-------------|
| `GET` | `/api/patients/` | ✅ | List all patients (owned by you) |
| `POST` | `/api/patients/` | ✅ | Create a new patient |
| `GET` | `/api/patients/<id>/` | ✅ | Retrieve patient details |
| `PUT` | `/api/patients/<id>/` | ✅ | Update patient (partial) |
| `DELETE` | `/api/patients/<id>/` | ✅ | Delete a patient |

### Doctors

| Method | Endpoint | Auth | Description |
|--------|----------|:----:|-------------|
| `GET` | `/api/doctors/` | ✅ | List all doctors |
| `POST` | `/api/doctors/` | ✅ | Create a new doctor |
| `GET` | `/api/doctors/<id>/` | ✅ | Retrieve doctor details |
| `PUT` | `/api/doctors/<id>/` | ✅ | Update doctor (partial) |
| `DELETE` | `/api/doctors/<id>/` | ✅ | Delete a doctor |

### Patient–Doctor Mappings

| Method | Endpoint | Auth | Description |
|--------|----------|:----:|-------------|
| `GET` | `/api/mappings/` | ✅ | List all your mappings |
| `POST` | `/api/mappings/` | ✅ | Assign a doctor to a patient |
| `GET` | `/api/mappings/<patient_id>/doctors/` | ✅ | Get all doctors for a patient |
| `DELETE` | `/api/mappings/<id>/` | ✅ | Remove a mapping |

> **Auth header:** `Authorization: Bearer <access_token>`

---

## 🔒 Authentication Flow

```
1. Register  →  POST /api/auth/register/
                 Body: { "name": "...", "email": "...", "password": "..." }
                 Response: { "tokens": { "access": "...", "refresh": "..." } }

2. Login     →  POST /api/auth/login/
                 Body: { "username": "...", "password": "..." }
                 Response: { "access": "...", "refresh": "..." }

3. Use token →  Authorization: Bearer <access_token>

4. Refresh   →  POST /api/auth/token/refresh/
                 Body: { "refresh": "..." }
                 Response: { "access": "..." }
```

---

## 🧪 Testing

```bash
# Run the full test suite (31 tests)
make test
# or: python manage.py test --verbosity=2
```

**Test coverage:**

| App | Tests | Covers |
|-----|:-----:|--------|
| `accounts` | 6 | Registration (success, validation, duplicates), login (success, failure) |
| `patients` | 10 | Auth, ownership isolation, CRUD, not-found, invalid data |
| `doctors` | 8 | Auth, CRUD, email uniqueness, not-found |
| `mappings` | 8 | Assignment, ownership, duplicates, patient-specific queries, deletion |

---

## 🛠️ Development Commands

| Command | Description |
|---------|-------------|
| `make help` | Show all available commands |
| `make run` | Start development server |
| `make test` | Run test suite |
| `make lint` | Run flake8 linter |
| `make format` | Auto-format with Black + isort |
| `make migrate` | Apply database migrations |
| `make makemigrations` | Generate new migrations |
| `make createsuperuser` | Create admin user |
| `make docker-up` | Start all services via Docker Compose |
| `make docker-down` | Stop Docker services |
| `make clean` | Remove `__pycache__` and `.pyc` files |

---

## ⚙️ Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | — |
| `DEBUG` | Debug mode | `True` |
| `DATABASE_NAME` | PostgreSQL database name | `healthcare_db` |
| `DATABASE_USER` | PostgreSQL user | `postgres` |
| `DATABASE_PASSWORD` | PostgreSQL password | — |
| `DATABASE_HOST` | Database host | `localhost` |
| `DATABASE_PORT` | Database port | `5432` |

---

## 📦 Tech Stack

- **Framework:** Django 6.0, Django REST Framework 3.17
- **Auth:** djangorestframework-simplejwt (JWT)
- **Database:** PostgreSQL 16 (via psycopg2-binary)
- **API Docs:** drf-spectacular (Swagger UI + OpenAPI 3.0)
- **Config:** python-decouple (.env)
- **CORS:** django-cors-headers
- **Code Quality:** Black, isort, flake8
- **Containerization:** Docker, Docker Compose

---

## 📄 License

MIT