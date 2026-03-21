# ASD Management — Project Specification

## 1. Overview

Application for the internal management of an Amateur Sports Association (ASD).
This is NOT a SaaS platform or an e-commerce site. It is a management tool used
internally by the ASD staff and members to handle registrations, documentation,
financial records, and athlete data.

**Architecture:**
- Backend: Django + Django REST Framework (API-only)
- Frontend: React (separate repository, consumes the APIs)
- Database: PostgreSQL
- Authentication: JWT (djangorestframework-simplejwt)
- Django Admin: reserved exclusively for the technical superadmin

---

## 2. User Roles

All roles access the application through the React frontend, except the
technical superadmin who uses Django Admin.

| Role | Description | Access |
|------|-------------|--------|
| **Superadmin** | Technical platform administrator | Django Admin only |
| **Admin** | ASD president/director, full operational access | React frontend |
| **Operator** | Administrative staff, manages registrations, payments, documents | React frontend |
| **Trainer** | Coach, manages own data and views assigned athletes | React frontend |
| **Member** | Athlete (adult) or parent/guardian of minor athletes | React frontend |

### Role permissions summary

- **Admin**: full access to all areas (users, athletes, staff, documents, finance)
- **Operator**: manages registrations, athlete records, documents, financial movements
- **Trainer**: views own athletes, manages own profile and schedule data
- **Member**: views and manages own profile and athletes under guardianship

### User-Athlete relationship (guardian pattern)

A User account represents anyone who logs in. An Athlete is a separate profile
representing someone who practices sport within the ASD. The link between them:

- `Athlete.guardian = FK(User)` — a User manages one or more Athletes
- Minor athlete: User = parent/guardian
- Adult athlete managing themselves: User = the athlete themselves (self-guardian)
- Adult athlete managed by someone else: User = family member, agent, etc.

---

## 3. Functional Areas

### 3.1 Registry Management (Anagrafiche)

CRUD operations for the main entities:

- **Athletes**: personal data, fiscal code, date/place of birth, category,
  assigned trainer, active/inactive status
- **Categories**: athlete age categories (code, description, age range)
- **Trainers**: personal data, fiscal code, optionally linked to a User account
- **Sport Doctors**: personal data, VAT number
- **Collaborators**: external collaborators (fiscal code, insertion date)
  *(future milestone)*
- **External Companies**: business name, used for invoice management
  *(future milestone)*

### 3.2 Enrollment and Medical Documentation

For each athlete, the ASD must manage:

- **Enrollment (Iscrizione)**: registration form for the sports season.
  Minors require a parent/guardian signature.
- **Sport Medical Certificate (Certificazione Medico-Sportiva)**: certifies
  physical fitness for competitive sport. Has an issue date, expiration date,
  and is linked to the issuing doctor and the athlete.

The operator registers both documents when the athlete joins the ASD.

### 3.3 Financial Management

The ASD tracks all financial movements:

- **Financial Movements**: date, description, amount, type (income/expense),
  category. Each movement can be linked to one of:
  - **Invoice (Fattura)**: purchase or sale invoice, linked to an external company
  - **Compensation (Compenso)**: payment to a collaborator
  - **User Purchase (Acquisto)**: purchase of a service by a user/member
- **Receipts**: automatic generation of fiscal receipts for user purchases
- **Services catalog**: internal list of activities/services offered by the ASD
  (courses, subscriptions), with description and price. Used for purchase tracking,
  not for online sales.

### 3.4 Institutional Grants (Bandi)

Area for managing documentation related to institutional grant applications.
Provides filtered views of athletes and their medical certificates based on
grant-specific criteria (age, active status, valid certification).

### 3.5 Admin Area

The ASD administrator (president) can:
- Manage operator profiles and their platform access authorization
- Manage user profiles and their access authorization
- Manage own profile
- Full access to all other areas

---

## 4. Legacy to New Architecture Mapping

The original application used a MySQL database. The legacy SQL schema is
preserved in `docs/legacy_schema.sql` for reference.

| Legacy Table | New Django App | New Model | Notes |
|---|---|---|---|
| `utenti` | `users` | `CustomUser` | Unified auth with roles |
| `amministratori` | `users` | `CustomUser` (role=admin) | No separate table |
| `operatori` | `users` | `CustomUser` (role=operator) | No separate table |
| `atleti` | `athletes` | `Athlete` | FK to User as guardian |
| `categorie` | `athletes` | `Category` | - |
| `medici` | `staff` | `SportDoctor` | - |
| `collaboratori` | `staff` | `Collaborator` | Future milestone |
| `certificazioni` | `enrollments` | `SportCertificate` | FK to Athlete + Doctor |
| `iscrizioni` | `enrollments` | `Enrollment` | FK to Athlete |
| `movimenti` | `finance` | `FinancialMovement` | - |
| `tipologie` | `finance` | `MovementType` | - |
| `fatture` | `finance` | `Invoice` | FK to Organization + Movement |
| `compensi` | `finance` | `Compensation` | FK to Collaborator + Movement |
| `acquisti` | `finance` | `Purchase` | FK to User + Service + Movement |
| `servizi` | `services` | `Service` | Internal catalog, not e-commerce |
| `societa` | `organizations` | `Organization` | External companies |
| `nazioni` | `geography` | `Country` | - |
| `province` | `geography` | `Province` | - |
| `comuni` | `geography` | `Municipality` | - |

---

## 5. Milestones

- **M1**: Foundation — project setup, Custom User model, JWT auth, Athletes,
  Trainers, Doctors, Categories (CRUD APIs + permissions + tests)
- **M2**: Enrollments + Sport Medical Certificates
- **M3**: Geography (countries, provinces, municipalities)
- **M4**: Finance base (movements, movement types, services catalog)
- **M5**: Finance advanced (invoices, compensations, purchases, receipts)
- **M6**: Reporting + Institutional Grants
- **M7**: Self-registration with approval + email notifications
- **M8**: Audit logging, file uploads, performance optimizations

---

## 6. Future Features (backlog)

- Public self-registration with operator approval
- Password reset via API
- Email notifications (certificate expiration, enrollment reminders)
- PDF generation (receipts, reports)
- Data import from legacy MySQL database (via management commands)
- Dashboard analytics endpoints
