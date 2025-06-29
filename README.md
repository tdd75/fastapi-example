# 🚀 FastAPI Example

A sample project built with [FastAPI](https://fastapi.tiangolo.com/) using SQLAlchemy for ORM, Alembic for database
migrations, and other modern tools to build a scalable, high-performance RESTful API.

---

## 📁 Project Structure

```
app/
├── api/                # Route definitions
├── config/             # App configuration
├── constant/           # Application constants
├── core/               # App core utilities
├── db/                 # DB connection & session
├── dto/                # Pydantic data transfer objects
├── helper/             # Helper functions and utilities
├── model/              # SQLAlchemy models
├── repository/         # Data access layer
├── use_case/           # Use case definitions
├── main.py             # FastAPI entry point
migrations/             # Alembic migration scripts
alembic.ini             # Alembic configuration
requirements.txt
README.md
```

---

## 🛠️ Setup Instructions

### 🍎 MacOS

```bash
brew install libpq && brew link --force libpq
python3 -m venv venv && source venv/bin/activate
pip3 install -r requirements.txt
```

### 🐧 Linux

```bash
sudo apt-get install libpq-dev
python3 -m venv venv && source venv/bin/activate
pip3 install -r requirements.txt
```

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

---

## 🌱 Seeding Initial Data

To populate the database with test data (e.g., 1,000,000 employees), run the following command:

```bash
PYTHONPATH=. python3 app/config/seed.py
```

> **Note:** Make sure your database
> is running and all migrations have been applied before executing the seed script.

---

## 🚀 Running the Application

```bash
uvicorn app.main:app --reload
```

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
