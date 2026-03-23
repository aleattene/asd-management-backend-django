# ASD Management — Backend

#### REST API backend for managing a Sports Association (ASD).

![Python](https://badgen.net/badge/Built%20with/Python/blue)
![Django](https://img.shields.io/badge/Built%20with-Django-092E20)
![Django Rest Framework](https://img.shields.io/badge/Built%20with-DRF-red)
[![Tests](https://github.com/aleattene/asd-management-backend/actions/workflows/tests.yml/badge.svg)](https://github.com/aleattene/asd-management-backend/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/aleattene/asd-management-backend/graph/badge.svg?token=452QWRN2E6)](https://codecov.io/gh/aleattene/asd-management-backend)
[![GitHub commits](https://badgen.net/github/commits/aleattene/asd-management-backend)](https://github.com/aleattene/asd-management-backend/commits/)
[![GitHub last commit](https://img.shields.io/github/last-commit/aleattene/asd-management-backend)](https://github.com/aleattene/asd-management-backend/commits/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://github.com/aleattene/asd-management-backend/pulls)
[![License](https://img.shields.io/github/license/aleattene/asd-management-backend?color=blue)](https://github.com/aleattene/asd-management-backend/blob/main/LICENSE)

*Work in Progress*

---

## Overview

Django REST Framework backend for the internal management of a Sports Association.
This is **not** an e-commerce or SaaS platform — it is a management tool used
by ASD staff and members to handle registrations, documentation, and athlete data.

The frontend (React) lives in a separate repository and consumes these APIs.

**Stack:**
- Python 3.13+
- Django 6.0+
- Django REST Framework 3.17+
- PostgreSQL (SQLite for local development)
- JWT authentication (djangorestframework-simplejwt)
- API documentation via drf-spectacular (Swagger UI)

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/aleattene/asd-management-backend.git
cd asd-management-backend
```

### 2. Create and activate a virtual environment
```bash
python3.13 -m venv .venv
source .venv/bin/activate        # macOS/Linux
.venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

For development (includes pytest, coverage, ruff):
```bash
pip install -r requirements_dev.txt
```

> **Dependency management:** this project uses [pip-tools](https://github.com/jazzband/pip-tools).
> The `requirements*.txt` files are compiled from `requirements*.in` and should not be edited directly.
> To add or update a dependency, edit the relevant `.in` file and recompile:
> ```bash
> pip-compile requirements.in
> pip-compile requirements_dev.in
> ```

---

## Configuration

The project reads configuration from environment variables. Create a `.env` file
in the project root with the following variables:

```bash
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000

# PostgreSQL (production only)
POSTGRES_DATABASE=asd_management
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

---

## Running the server

### 1. Apply migrations
```bash
python manage.py migrate
```

### 2. Create a superuser (technical admin only)
```bash
python manage.py createsuperuser
```

### 3. Start the development server
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/v1/`.

---

## API Documentation

Swagger UI is available at:
```
http://localhost:8000/api/schema/swagger-ui/
```

OpenAPI schema (JSON) at:
```
http://localhost:8000/api/schema/
```

### Main endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/token/` | Obtain JWT token pair |
| POST | `/api/v1/auth/token/refresh/` | Refresh access token |
| GET/PATCH | `/api/v1/users/me/` | Own profile |
| GET/POST | `/api/v1/users/` | List/create users (admin/operator) |
| PATCH | `/api/v1/users/{id}/set_role/` | Change user role (superadmin only) |
| GET/POST | `/api/v1/athletes/` | List/create athletes |
| GET/POST | `/api/v1/categories/` | List/create categories |
| GET/POST | `/api/v1/trainers/` | List/create trainers |
| GET/POST | `/api/v1/doctors/` | List/create sport doctors |
| GET/POST | `/api/v1/enrollments/` | List/create season enrollments |
| GET/POST | `/api/v1/certificates/` | List/create sport medical certificates |
| GET/POST | `/api/v1/countries/` | List/create countries (write: admin/operator; read-only: any authenticated user) |
| GET/POST | `/api/v1/provinces/` | List/create Italian provinces (write: admin/operator; read-only: any authenticated user) |
| GET/POST | `/api/v1/municipalities/` | List/create municipalities, filter by `?province=<id>` (write: admin/operator; read-only: any authenticated user) |

---

## Running tests

```bash
python manage.py test --settings=config.settings.test
```

With coverage:
```bash
coverage run manage.py test --settings=config.settings.test
coverage report --show-missing
```

---

## Project structure

```
config/
    settings/           # base / development / production / test
    urls.py             # API-only routing + Django Admin
    permissions.py      # Role-based permission classes
    pagination.py       # Standard pagination
users/                  # Custom user model with roles + JWT
athletes/               # Athlete registry + categories
staff/                  # Trainers (internal ASD staff)
doctors/                # Sport doctors (external professionals)
enrollments/            # Season enrollments
certificates/           # Sport medical certificates
geography/              # Reference data: countries, provinces, municipalities
docs/                   # Additional project documentation
```

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Commit following [Conventional Commits](https://www.conventionalcommits.org/)
4. Open a pull request to `main`

---

## License

This project is licensed under the [MIT License](LICENSE).
