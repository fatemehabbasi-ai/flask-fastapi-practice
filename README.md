# Flask & FastAPI Practice Project

A small practice project implementing the same simple authentication API twice — once with **Flask** and once with **FastAPI** — to compare the two frameworks side by side.

## What it does

Both versions implement the same core features:

- `GET /` — a basic "Hello" route
- `GET /greet/<name>` — a dynamic route that returns a personalized greeting
- `GET /age/<age>` — a dynamic route with type validation, calculates years left until age 100
- `POST /register` — registers a new user (stores a **hashed** password in a SQLite database, rejects duplicate usernames)
- `POST /login` — authenticates a user against the database using hashed password verification

## Tech stack

**Flask version (`app.py`)**
- Flask
- Flask-SQLAlchemy (SQLite database)
- Werkzeug security (`generate_password_hash` / `check_password_hash`)

**FastAPI version (`main.py`)**
- FastAPI + Uvicorn
- SQLAlchemy (raw, with dependency injection via `Depends`)
- Pydantic models for request validation
- Werkzeug security for password hashing
- Auto-generated interactive docs at `/docs` (Swagger UI)

## How to run

### Flask
```bash
pip install flask flask_sqlalchemy werkzeug
python app.py
```
Runs on `http://127.0.0.1:5000`

### FastAPI
```bash
pip install fastapi uvicorn sqlalchemy werkzeug
python -m uvicorn main:app --reload
```
Runs on `http://127.0.0.1:8000`
Interactive docs: `http://127.0.0.1:8000/docs`

## What I learned

This project was built step by step to practice:
- Static vs. dynamic routes, and route type converters
- Handling GET vs. POST requests
- Reading JSON request bodies and returning JSON responses
- Using proper HTTP status codes (200, 201, 400, 401, 404, 422)
- Connecting a Flask/FastAPI app to a SQLite database with an ORM
- Hashing passwords instead of storing them in plain text
- Testing an API with `curl`, PowerShell's `Invoke-WebRequest`, Python's `requests`, and FastAPI's built-in Swagger UI

## Notes

This is a learning/practice project, not production-ready. Next steps to make it production-grade would include: token-based authentication (JWT), input sanitization, environment-based config instead of hardcoded database URIs, and proper error logging.