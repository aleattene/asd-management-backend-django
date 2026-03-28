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

#### Auth
| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| POST | `/api/v1/auth/token/` | Obtain JWT token pair | Public |
| POST | `/api/v1/auth/token/refresh/` | Refresh access token | Public |

#### Users
| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| GET/PATCH | `/api/v1/users/me/` | Own profile | Authenticated (non-external) |
| GET/POST | `/api/v1/users/` | List/create users | Admin/Operator/Superadmin |
| GET/PATCH/DELETE | `/api/v1/users/{id}/` | User detail | Admin/Operator/Superadmin |
| PATCH | `/api/v1/users/{id}/set_role/` | Change user role | Superadmin only |

#### Registry
| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| GET/POST | `/api/v1/athletes/` | List/create athletes | Read: authenticated (non-external); Write: Admin/Operator/Superadmin |
| GET/PATCH/DELETE | `/api/v1/athletes/{id}/` | Athlete detail | Read: authenticated (non-external); Write: Admin/Operator/Superadmin |
| GET/POST | `/api/v1/categories/` | List/create categories | Read: authenticated (non-external); Write: Admin/Operator/Superadmin |
| GET/PATCH/DELETE | `/api/v1/categories/{id}/` | Category detail | Read: authenticated (non-external); Write: Admin/Operator/Superadmin |
| GET/POST | `/api/v1/trainers/` | List/create trainers | Admin/Operator/Superadmin |
| GET/PATCH/DELETE | `/api/v1/trainers/{id}/` | Trainer detail | Admin/Operator/Superadmin |
| GET/POST | `/api/v1/doctors/` | List/create sport doctors | Admin/Operator/Superadmin |
| GET/PATCH/DELETE | `/api/v1/doctors/{id}/` | Doctor detail | Admin/Operator/Superadmin |

#### Enrollments & Certificates
| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| GET/POST | `/api/v1/enrollments/` | List/create season enrollments | Read: authenticated (non-external); Write: Admin/Operator/Superadmin |
| GET/PATCH/DELETE | `/api/v1/enrollments/{id}/` | Enrollment detail | Read: authenticated (non-external); Write: Admin/Operator/Superadmin |
| GET/POST | `/api/v1/certificates/` | List/create sport medical certificates | Read: authenticated (non-external); Write: Admin/Operator/Superadmin |
| GET/PATCH/DELETE | `/api/v1/certificates/{id}/` | Certificate detail | Read: authenticated (non-external); Write: Admin/Operator/Superadmin |

#### Geography (lookup data)
| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| GET/POST | `/api/v1/countries/` | List/create countries | Read: authenticated (non-external); Write: Admin/Operator/Superadmin |
| GET/PATCH/DELETE | `/api/v1/countries/{id}/` | Country detail | Read: authenticated (non-external); Write: Admin/Operator/Superadmin |
| GET/POST | `/api/v1/provinces/` | List/create Italian provinces | Read: authenticated (non-external); Write: Admin/Operator/Superadmin |
| GET/PATCH/DELETE | `/api/v1/provinces/{id}/` | Province detail | Read: authenticated (non-external); Write: Admin/Operator/Superadmin |
| GET/POST | `/api/v1/municipalities/` | List/create municipalities (`?province=<id>`) | Read: authenticated (non-external); Write: Admin/Operator/Superadmin |
| GET/PATCH/DELETE | `/api/v1/municipalities/{id}/` | Municipality detail | Read: authenticated (non-external); Write: Admin/Operator/Superadmin |

#### Finance
| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| GET/POST | `/api/v1/companies/` | List/create companies | Admin/Operator/Superadmin |
| GET/PATCH/DELETE | `/api/v1/companies/{id}/` | Company detail | Admin/Operator/Superadmin |
| GET/POST | `/api/v1/payment-methods/` | List/create payment methods | Admin/Operator/Superadmin |
| GET/PATCH/DELETE | `/api/v1/payment-methods/{id}/` | Payment method detail | Admin/Operator/Superadmin |
| GET/POST | `/api/v1/invoices/` | List/create invoices (`direction=purchase` or `direction=sale`) | Admin/Operator/Superadmin |
| GET/PATCH/DELETE | `/api/v1/invoices/{id}/` | Invoice detail | Admin/Operator/Superadmin |
| GET/POST | `/api/v1/receipts/` | List/create receipts | Admin/Operator/Superadmin |
| GET/PATCH/DELETE | `/api/v1/receipts/{id}/` | Receipt detail | Admin/Operator/Superadmin |

---

## Development data

To populate the local database with realistic seed data (users, athletes, enrollments, invoices, etc.),
the following environment variables must be set in your `.env` file (see `.env.example`):

```bash
SEED_SUPERADMIN_USERNAME=
SEED_SUPERADMIN_EMAIL=
SEED_SUPERADMIN_PASSWORD=
SEED_ADMIN_USERNAME=
SEED_ADMIN_EMAIL=
SEED_ADMIN_PASSWORD=
```

Requires `DEBUG=True` and dev dependencies installed (`pip install -r requirements_dev.txt`).

```bash
python manage.py seed_db
```

To reset and re-seed from scratch (preserves existing superusers):

```bash
python manage.py seed_db --flush
```

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
companies/              # External companies (invoicing counterparts)
payment_methods/        # Configurable payment methods
invoices/               # Purchase and sale invoices
receipts/               # Fiscal receipts (member payments + staff compensations)
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
