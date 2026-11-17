# ReturnGuard

**AI-Assisted E-commerce Returns and Refunds Backend**

ReturnGuard is a backend application designed to manage customer returns and refunds for an e-commerce platform. It provides REST APIs for customer management, order management, and return request processing.

## Project Objectives

- Build RESTful APIs using FastAPI.
- Implement a layered backend architecture.
- Manage relational data using SQLAlchemy.
- Validate API requests using Pydantic.
- Enforce return request business rules.
- Implement automated API testing.
- Prepare the foundation for AI-assisted return classification.

## Technology Stack

| Technology | Purpose                         |
| ---------- | ------------------------------- |
| Python     | Backend programming language    |
| FastAPI    | REST API framework              |
| SQLAlchemy | ORM and database access         |
| SQLite     | Relational database             |
| Pydantic   | Request and response validation |
| Pytest     | Automated testing               |
| HTTPX      | API test client                 |

## Architecture

The application follows a layered architecture:

```text
Client
  |
  v
API Router
  |
  v
Service Layer
  |
  v
SQLAlchemy ORM
  |
  v
SQLite Database
```

### Project Structure

```text
app/
├── api/v1/       # API endpoints and routing
├── core/         # Application configuration
├── db/           # Database engine and sessions
├── models/       # SQLAlchemy models
├── schemas/      # Pydantic schemas
├── services/     # Business logic
└── main.py       # Application entry point

tests/
├── conftest.py   # Shared test fixtures
└── test_api.py   # API test cases
```

## Implemented Features

### Customer Management

- Create customers
- Retrieve customers
- List customers
- Validate email addresses
- Prevent duplicate customer emails

### Order Management

- Create orders
- Retrieve orders
- List orders
- Validate customer references

### Return Management

- Submit return requests
- Retrieve return requests
- List return requests
- Validate order eligibility
- Prevent duplicate active return requests
- Initialize requests with pending status

### Automated Testing

- Health endpoint tests
- Customer API tests
- Order API tests
- Return API tests
- Validation and negative scenario tests

## Local Setup

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd ReturnGuard
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
uvicorn app.main:app --reload
```

### 5. Access API documentation

Swagger UI:

http://127.0.0.1:8000/docs

Health check:

http://127.0.0.1:8000/health

## Running Tests

Execute the automated test suite:

```bash
python -m pytest -v
```

The test suite uses an isolated in-memory SQLite database.

## API Endpoints

| Method | Endpoint                 | Description             |
| ------ | ------------------------ | ----------------------- |
| GET    | `/health`                | Health check            |
| POST   | `/api/v1/customers`      | Create customer         |
| GET    | `/api/v1/customers`      | List customers          |
| GET    | `/api/v1/customers/{id}` | Retrieve customer       |
| POST   | `/api/v1/orders`         | Create order            |
| GET    | `/api/v1/orders`         | List orders             |
| GET    | `/api/v1/orders/{id}`    | Retrieve order          |
| POST   | `/api/v1/returns`        | Create return request   |
| GET    | `/api/v1/returns`        | List return requests    |
| GET    | `/api/v1/returns/{id}`   | Retrieve return request |

## Planned Enhancements

- PostgreSQL database integration
- Alembic database migrations
- Authentication and role-based authorization
- Return eligibility based on delivery date
- Refund processing workflow
- Improved transaction and concurrency handling
- Structured logging and error handling
- AI-assisted return reason classification
- Docker support
- CI/CD pipeline

## Project Status

**Phase 1 — Core Backend Foundation**

Customer, order, and return request APIs have been implemented, with automated tests covering the main API scenarios.

Further enhancements will be developed incrementally.
