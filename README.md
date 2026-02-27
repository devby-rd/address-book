# Address Book API

A minimal REST API built using FastAPI and SQLite that allows users to:

- Create an address
- Update an address
- Delete an address
- Retrieve all addresses
- Retrieve addresses within a given radius (in kilometers)
- Validate input data (email, coordinates, etc.)

---

## Tech Stack

- Python 3.10+
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic (v2)
- Pytest

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/devby-rd/address-book.git
cd address_book
```

---

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not available:

```bash
pip install fastapi uvicorn sqlalchemy pydantic[email] pytest
```

---

## Run the Application

```bash
uvicorn app.main:app --reload
```

Open your browser and visit:

```
http://127.0.0.1:8000/docs
```

FastAPI’s built-in Swagger UI can be used to test all endpoints.

---

## Run Tests

```bash
pytest
```

---

## Features

- SQLite database persistence
- Input validation using Pydantic
- Email format validation
- Latitude/Longitude validation
- Nearby address search using Haversine distance calculation
- Structured logging
- Isolated in-memory database for tests
- RESTful API design

---

## Notes

- The application uses SQLite for simplicity.
- Tests use an in-memory SQLite database to ensure isolation.
- No GUI is required — FastAPI Swagger UI is sufficient.