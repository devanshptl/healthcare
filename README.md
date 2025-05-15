# Healthcare Backend API

This is a Django REST Framework-based backend for managing users, patients, doctors, and patient-doctor mappings with JWT authentication.

---

## Features

- User registration and login with JWT authentication  
- CRUD operations for Patients and Doctors  
- Patient-Doctor mappings management  
- Secure endpoints accessible only to authenticated users  
- PostgreSQL database backend  

---

## Project Setup

### Prerequisites

- Python 3.8+  
- PostgreSQL 12+  
- `pip` package manager  
- `virtualenv` (recommended)  

---

### Steps to Setup Project

1. **Clone the repository**:

```bash
git clone https://github.com/devanshptl/healthcare.git
cd healthcare
```

2. **Create and activate a virtual environment**:

```bash
# Create virtual environment (use python3 or python accordingly)
python -m venv venv

# Activate on Linux/macOS
source venv/bin/activate

# Activate on Windows (PowerShell)
venv\Scripts\Activate.ps1
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

4. **Set up PostgreSQL**:

- Install PostgreSQL if not installed:  
```bash
sudo apt install postgresql postgresql-contrib
```

- Open PostgreSQL shell:
```bash
sudo -u postgres psql
```

- Run these commands inside the PostgreSQL shell:

```sql
CREATE DATABASE your_db;
CREATE USER healthcare_user WITH PASSWORD 'yourpassword';
ALTER ROLE healthcare_user SET client_encoding TO 'utf8';
ALTER ROLE healthcare_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE healthcare_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE your_db TO your_user;
\q
```

5. **Create a `.env` file** in your project root:

```env
DJANGO_SECRET_KEY=your_django_secret_key
DEBUG=True

POSTGRES_DB=your_db
POSTGRES_USER=your_user
POSTGRES_PASSWORD=yourpassword
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

```

6. **Apply migrations**:

```bash
python manage.py migrate
```

7. **(Optional) Create a superuser** for Django admin:

```bash
python manage.py createsuperuser
```

8. **Run the development server**:

```bash
python manage.py runserver
```

> The API will be available at: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## API Endpoints Overview

### Authentication

- `POST /auth/register/` — User registration  
- `POST /auth/login/` — User login (get JWT tokens)  
- `POST /auth/refresh/` — Refresh access token  

### Patients

- `POST /patients/` — Create patient (authenticated)  
- `GET /patients/` — List patients (owned by user)  
- `GET /patients/<pk>/` — Retrieve patient by ID  
- `PUT/PATCH /patients/<pk>/` — Update patient by ID  
- `DELETE /patients/<pk>/` — Delete patient by ID  

### Doctors

- `POST /doctors/` — Create doctor (authenticated)  
- `GET /doctors/` — List doctors  
- `GET /doctors/<pk>/` — Retrieve doctor by ID  
- `PUT/PATCH /doctors/<pk>/` — Update doctor by ID  
- `DELETE /doctors/<pk>/` — Delete doctor by ID  

### Patient-Doctor Mappings

- `POST /mappings/` — Create patient-doctor mapping  
- `GET /mappings/` — List all mappings  
- `GET /mappings/patient/<patient_id>/` — List mappings for a patient  
- `DELETE /mappings/<pk>/` — Delete mapping by ID  

---

## Additional Notes

- Authentication is handled via JWT using the `Authorization: Bearer <access_token>` header.  
- Use the provided refresh token to obtain new access tokens.  
- Ensure your `.env` file is added to `.gitignore` to avoid committing secrets.  

---

