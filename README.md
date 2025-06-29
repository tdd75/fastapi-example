# 🚀 FastAPI Example

A sample project built with [FastAPI](https://fastapi.tiangolo.com/) using SQLAlchemy for ORM, Alembic for database
migrations, and other modern tools to build a scalable, high-performance RESTful API.

---

## 📦 Tech Stack

- **FastAPI** – Web framework for building APIs
- **SQLAlchemy** – ORM for database interactions
- **Alembic** – Database migration tool
- **PostgreSQL** – Primary database
- **Uvicorn** – ASGI server
- **Pydantic** – Data validation and serialization

---

## 🛠️ Setup

### 1. Install system dependencies

```bash
# Linux (Ubuntu/Debian)
sudo apt-get install libpq-dev

# macOS (Homebrew)
brew install libpq && brew link --force libpq
```

### 2. Create and activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```


### 4. Run database migrations

```bash
# Start the PostgreSQL database (choose one option):

# Option 1: Use local PostgreSQL service
# (Ensure PostgreSQL is running on your machine)

# Option 2: Use Docker Compose to start the database container
docker compose up

# Run database migrations after the database is ready
alembic upgrade head
```

---

## 🧪 Running the Application

```bash
uvicorn app.main:app --reload
```

- `--reload`: Automatically reloads the server on code changes (for development)
- Default URL: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs

---

## 🧬 Database Migration (Alembic)

### Create a new migration

```bash
alembic revision --autogenerate -m "your migration message"
```

### Apply latest migrations

```bash
alembic upgrade head
```

### Roll back one migration

```bash
alembic downgrade -1
```

> Alembic configuration is located in `alembic.ini` and the `migrations/` directory.

---

## 📁 Project Structure

```
app/
├── config/             # App configuration
├── core/               # App core utilities
├── database/           # DB connection & session
├── constant/           # Application constants
├── api/                # Route definitions
├── dto/                # Pydantic data transfer objects
├── use_case/           # Use case definitions
├── service/            # Business logic
├── repository/         # Data access layer
├── model/              # SQLAlchemy models
├── main.py             # FastAPI entry point
migrations/             # Alembic migration scripts
alembic.ini             # Alembic configuration
requirements.txt
README.md
```

---

## 📄 License

This project is licensed under the MIT License.

---

## 🐳 Deployment with Docker

### 1. Build Docker image

```bash
docker compose build
```

### 2. Run the container

```bash
docker compose up --profile prod -d
```

### 3. Stop and remove the container

```bash
docker comopse down
```

---

## 🌱 Seeding Initial Data

To populate the database with test data (e.g., 1,000,000 employees), run the following command:

```bash
PYTHONPATH=. python3 app/config/seed.py
```

> **Note:** Make sure your database
> is running and all migrations have been applied before executing the seed script.
# fastapi-example
# fastapi-example
