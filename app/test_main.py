from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app import models
from app.database import Base, get_db
from app.main import app
from app.models import Account, Transaction 


SQLALCHEMY_TEST_DATABASE_URL = "postgresql://postgres:mysecretpassword@postgres_db:5432/accounts_transactions_test"

engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the tables in the test DB
models.Base.metadata.create_all(bind=engine)

# Override the get_db dependency to use the test DB session
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Apply override before initializing client
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True, scope="session")
def clear_db():
    """Delete all rows before each test."""
    db = TestingSessionLocal()
    try:
        db.execute(text("DELETE FROM transactions;"))
        db.execute(text("DELETE FROM accounts;"))
        db.commit()
    finally:
        db.close()


def test_create_account():
    response = client.post(
        "/accounts/",
        json={"name": "Test User", "email": "test@example.com", "balance": 100.0}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test User"
    assert data["email"] == "test@example.com"
    assert data["balance"] == 100.0
    assert "id" in data


def test_create_duplicate_account():
    client.post(
        "/accounts/",
        json={"name": "Test User",
              "email": "duplicate@example.com", "balance": 100.0}
    )

    response = client.post(
        "/accounts/",
        json={"name": "Another User",
              "email": "duplicate@example.com", "balance": 200.0}
    )

    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]


def test_update_account():
    create_response = client.post(
        "/accounts/",
        json={"name": "Original Name",
              "email": "update@example.com", "balance": 100.0}
    )
    account_id = create_response.json()["id"]

    update_response = client.put(
        f"/accounts/{account_id}",
        json={"name": "Updated Name", "phone": "123456789"}
    )

    assert update_response.status_code == 200
    data = update_response.json()
    assert data["name"] == "Updated Name"
    assert data["phone"] == "123456789"
    assert data["email"] == "update@example.com"


def test_create_transaction():
    account_response = client.post(
        "/accounts/",
        json={"name": "Transaction User",
              "email": "transaction@example.com", "balance": 1000.0}
    )
    account_id = account_response.json()["id"]

    transaction_response = client.post(
        "/transactions/",
        json={"account_id": account_id, "amount": 500.0,
              "transaction_type": "deposit"}
    )

    assert transaction_response.status_code == 201
    data = transaction_response.json()
    assert data["account_id"] == account_id
    assert data["amount"] == 500.0
    assert data["transaction_type"] == "deposit"

    updated_account = client.get(f"/accounts/{account_id}").json()
    assert updated_account["balance"] == 1500.0


def test_withdrawal_insufficient_funds():
    account_response = client.post(
        "/accounts/",
        json={"name": "Poor User", "email": "poor@example.com", "balance": 100.0}
    )
    account_id = account_response.json()["id"]

    transaction_response = client.post(
        "/transactions/",
        json={"account_id": account_id, "amount": 200.0,
              "transaction_type": "withdrawal"}
    )

    assert transaction_response.status_code == 400
    assert "Insufficient funds" in transaction_response.json()["detail"]

    updated_account = client.get(f"/accounts/{account_id}").json()
    assert updated_account["balance"] == 100.0


def test_get_transactions():
    account_response = client.post(
        "/accounts/",
        json={"name": "Transactions User",
              "email": "transactions@example.com", "balance": 1000.0}
    )
    account_id = account_response.json()["id"]

    client.post("/transactions/", json={"account_id": account_id,
                "amount": 100.0, "transaction_type": "deposit"})
    client.post("/transactions/", json={"account_id": account_id,
                "amount": 50.0, "transaction_type": "withdrawal"})

    all_tx = client.get("/transactions/").json()
    assert len(all_tx) == 3

    account_tx = client.get(f"/transactions/?account_id={account_id}").json()
    assert len(account_tx) == 2
    assert all(tx["account_id"] == account_id for tx in account_tx)
