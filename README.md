# aw-api

A REST API built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**, built as a hands-on learning project on top of the AdventureWorks sample database.

This project started as a way to practice SQL against the AdventureWorks `humanresources` and `production` schemas, then grew into a full FastAPI learning exercise covering routing, request validation, pagination, and the move from raw SQL to a proper SQLAlchemy ORM layer.

## Tech stack

- **FastAPI** — web framework
- **SQLAlchemy** (Core + ORM) — database access
- **PostgreSQL** — database (AdventureWorks sample dataset)
- **Pydantic** — request/response validation and shaping
- **uv** — Python package and project management

## Project structure

```
src/aw_api/
├── main.py              # app entrypoint, mounts routers
├── database.py           # engine, session, get_db dependency
├── routers/               # route handlers, one file per resource
├── repositories/          # database queries, one file per resource
├── models/                # SQLAlchemy ORM models
└── schemas/                # Pydantic request/response models
```

The project follows a layered pattern: **router → repository → ORM model → database**. Routers handle HTTP concerns (status codes, request/response shape) and never touch SQL directly; repositories own all database queries and return plain data or `None`/booleans; routers interpret that data into the right HTTP response.

## Endpoints

### Employees (`humanresources` schema)

| Method | Path | Description |
|---|---|---|
| GET | `/employee/{id}` | Get a single employee by ID |
| GET | `/departments/{id}/employees` | Get all current employees in a department |

### Job Candidates (`humanresources` schema)

| Method | Path | Description |
|---|---|---|
| POST | `/jobcandidates` | Create a new job candidate (resume validated as XML) |
| DELETE | `/jobcandidates/{id}` | Delete a job candidate by ID |
| PATCH | `/jobcandidates/{id}` | Partially update a job candidate's resume |

### Products (`production` schema)

| Method | Path | Description |
|---|---|---|
| GET | `/products` | List products (paginated with `limit`/`offset`) |
| GET | `/products/{id}` | Get a single product by ID |
| GET | `/categories` | List all product categories |
| GET | `/category/{id}` | Get a single product category |
| GET | `/category/{id}/subcategory` | List subcategories under a category |
| GET | `/category/{id}/subcategory-detailed` | List subcategories with their parent category's name included |

## Running locally

```bash
uv sync
uv run fastapi dev src/aw_api/main.py
```

Create a `.env` file in the project root with:

```
DATABASE_URL=postgresql+psycopg2://<username>:<password>@localhost:5432/<database_name>
```

Interactive API docs are available at `/docs` once the server is running.

## What this project covers

- REST routing with path and query parameters
- Request body validation with Pydantic, including a custom field validator (XML resume check)
- Response shaping with `response_model`, keeping internal database columns out of API responses
- Pagination with `limit`/`offset` and a deterministic `ORDER BY`
- Multi-table joins, both in raw SQL and SQLAlchemy's Core `select()` syntax
- Proper error handling: repositories return data/`None`/booleans, routers decide the HTTP response
- A full migration from raw parameterized SQL to a SQLAlchemy ORM layer (models, `select`/`insert`/`update`/`delete`)
