from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
import enum
from sqlalchemy.sql import func

Base = declarative_base()


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    balance = Column(Float, default=0.0, nullable=False)
    phone = Column(String(20), nullable=True)
    address = Column(String(200), nullable=True)

    transactions = relationship("Transaction", back_populates="account")


class TransactionType(str, enum.Enum):
    deposit = "deposit"
    withdrawal = "withdrawal"


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    amount = Column(Float, nullable=False)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    timestamp = Column(DateTime, nullable=False, default=func.now())

    account = relationship("Account", back_populates="transactions")
