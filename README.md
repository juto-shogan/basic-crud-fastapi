
# Basic CRUD API with FastAPI

A simple REST API built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**, demonstrating basic CRUD operations and a structured application architecture.

## Tech Stack

* Python 3.13+
* FastAPI
* SQLAlchemy
* PostgreSQL
* Pydantic
* uv

## Project Structure

```text
src/
└── aw_api/
    ├── models/
    ├── repositories/
    ├── routers/
    ├── schemas/
    ├── database.py
    └── main.py
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/juto-shogan/basic-crud-fastapi.git
cd basic-crud-fastapi
```

### 2. Install uv

If you do not already have `uv` installed, follow the official installation guide:

```bash
uv --version
```

### 3. Install dependencies

```bash
uv sync
```

This creates the project environment and installs the dependencies defined in `pyproject.toml`. The included `uv.lock` file ensures reproducible dependency versions.

### 4. Configure environment variables

Create a `.env` file in the project root and add your PostgreSQL connection details:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
```

### 5. Run the API

```bash
uv run fastapi dev src/aw_api/main.py
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation is available at:

* `/docs` — Swagger UI
* `/redoc` — ReDoc

## Features

* RESTful API endpoints
* CRUD operations
* PostgreSQL database integration
* SQLAlchemy database sessions
* Pydantic request and response validation
* Modular router and repository structure
* Interactive API documentation

## Purpose

This project was built to practice developing backend APIs with **FastAPI**, database integration, CRUD operations, and clean project organization.
