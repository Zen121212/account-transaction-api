from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import engine, get_db,Base
from typing import List, Optional
from datetime import datetime
import uvicorn
import secrets

# FastAPI instance
app = FastAPI(
    title="Account and Transaction Management API",
    description="RESTful API for managing accounts and transactions",
    version="1.0.0"
)

# Create database tables on startup
@app.on_event("startup")
def startup():
    models.Base.metadata.create_all(bind=engine)

# Account endpoints
@app.post("/accounts/", response_model=schemas.Account, status_code=201)
async def create_account(account: schemas.AccountCreate, request: Request, db: Session = Depends(get_db)):
    db_account = db.query(models.Account).filter(models.Account.email == account.email).first()
    if db_account:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_account = models.Account(**account.dict())
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

# @app.post("/accounts/bulk", response_model=List[schemas.Account], status_code=201)
# async def create_multiple_accounts(accounts: List[schemas.AccountCreate], request: Request, db: Session = Depends(get_db)):
#     created_accounts = []
#     for account in accounts:
#         if db.query(models.Account).filter(models.Account.email == account.email).first():
#             continue
#         new_account = models.Account(**account.dict())
#         db.add(new_account)
#         created_accounts.append(new_account)

#     db.commit()
#     for acc in created_accounts:
#         db.refresh(acc)

#     return created_accounts

@app.put("/accounts/{account_id}", response_model=schemas.Account)
async def update_account(account_id: int, account: schemas.AccountUpdate, request: Request, db: Session = Depends(get_db)):
    db_account = db.query(models.Account).filter(models.Account.id == account_id).first()
    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")

    update_data = account.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_account, key, value)

    db.commit()
    db.refresh(db_account)
    return db_account

@app.get("/accounts/{account_id}", response_model=schemas.Account)
async def get_account(account_id: int, db: Session = Depends(get_db)):
    db_account = db.query(models.Account).filter(models.Account.id == account_id).first()
    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account

@app.get("/accounts/", response_model=List[schemas.Account])
async def get_accounts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    accounts = db.query(models.Account).offset(skip).limit(limit).all()
    return accounts

# Transaction endpoints
@app.post("/transactions/", response_model=schemas.Transaction, status_code=201)
async def create_transaction(transaction: schemas.TransactionCreate, request: Request, db: Session = Depends(get_db)):
    db_account = db.query(models.Account).filter(models.Account.id == transaction.account_id).first()
    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")

    db_transaction = models.Transaction(
        account_id=transaction.account_id,
        amount=transaction.amount,
        transaction_type=transaction.transaction_type,
        timestamp=transaction.timestamp or datetime.now()
    )

    if transaction.transaction_type == "deposit":
        db_account.balance += transaction.amount
    elif transaction.transaction_type == "withdrawal":
        if db_account.balance < transaction.amount:
            raise HTTPException(status_code=400, detail="Insufficient funds")
        db_account.balance -= transaction.amount
    else:
        raise HTTPException(status_code=400, detail="Invalid transaction type")

    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@app.get("/transactions/", response_model=List[schemas.Transaction])
async def get_transactions(
    account_id: Optional[int] = None,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(models.Transaction)

    if account_id:
        query = query.filter(models.Transaction.account_id == account_id)
    if from_date:
        query = query.filter(models.Transaction.timestamp >= from_date)
    if to_date:
        query = query.filter(models.Transaction.timestamp <= to_date)

    transactions = query.offset(skip).limit(limit).all()
    return transactions

@app.get("/transactions/{transaction_id}", response_model=schemas.Transaction)
async def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    db_transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
