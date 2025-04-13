# schemas.py
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
from .models import TransactionType

# Account schemas

class AccountBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None


class AccountCreate(AccountBase):
    balance: float = Field(ge=0.0, default=0.0)

    @validator('balance')
    def balance_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('Balance must be greater than or equal to 0')
        return v


class AccountUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class Account(AccountBase):
    id: int
    balance: float

    class Config:
        orm_mode = True


# Transaction schemas

class TransactionBase(BaseModel):
    account_id: int
    amount: float = Field(gt=0.0)
    transaction_type: TransactionType

    @validator('amount')
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Amount must be greater than 0')
        return v


class TransactionCreate(TransactionBase):
    timestamp: Optional[datetime] = None


class Transaction(TransactionBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True
