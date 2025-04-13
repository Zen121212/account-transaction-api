# Account & Transaction Management API

A RESTful API built with FastAPI to manage user accounts and transactions. It supports creating and updating accounts, recording deposit and withdrawal transactions, and retrieving transaction history. PostgreSQL is used as the database backend.

---

## Features

- Create an account (`POST /accounts/`)
- Update an account (`PUT /accounts/{account_id}`)
- Create a transaction (`POST /transactions/`)
- Get all transactions (`GET /transactions/`)
- FastAPI auto-generated Swagger UI (`/docs`) and ReDoc (`/redoc`)

---

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Docker & Docker Compose
- Pytest (for testing)

---

## Installation & Setup

### Prerequisites

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- `make` or Unix-like shell (for scripts)

### Steps

1. Clone the repo:

```bash
git clone https://github.com/yourusername/your-repo.git
cd your-repo
```

2. Start the containers:

```bash
./start.sh
```

3. Access API docs:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

4. Access pgAdmin: [http://localhost:5051](http://localhost:5051)

---

## API Endpoints

### 📘 Create Account

**POST** `/accounts/`

```json
{
  "name": "Zein",
  "email": "zein@example.com",
  "balance": 500.0,
  "phone": "12345678",
  "address": "Beirut"
}
```

---

### 📗 Update Account

**PUT** `/accounts/{account_id}`

```json
{
  "name": "Zein Updated",
  "email": "zein@example.com",
  "balance": 1000.0
}
```

---

### 💰 Create Transaction

**POST** `/transactions/`

```json
{
  "account_id": 1,
  "amount": 200.0,
  "transaction_type": "deposit"
}
```

---

### 📄 Get Transactions

**GET** `/transactions/`

Optional query params: `account_id`, `start_date`, `end_date`

---

## Running Tests

To run tests using `pytest`, use the following command:

```bash
docker-compose exec backend pytest app/test_main.py
```

Test coverage includes:

- Creating an account
- Updating an account
- Creating a transaction (deposit/withdrawal)
- Validating insufficient funds
- Retrieving all transactions
- Filtering transactions by account

---

## Design Decisions

- Used FastAPI for speed and automatic documentation generation.
- PostgreSQL chosen for reliability and compatibility with Docker.
- SQLAlchemy for ORM to ensure scalability and easier migration.

---

## Assumptions

- Email is treated as a unique identifier for accounts.
- Transactions must link to a valid account.

---

## Author

Zein Kassem - [zein.s.kassem@gmail.com](mailto:zein.s.kassem@gmail.com)
