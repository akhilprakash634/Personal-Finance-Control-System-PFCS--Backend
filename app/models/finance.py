from sqlalchemy import Column, Integer, String, Float
from app.db.database import Base

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String) # bank/wallet/cash
    balance = Column(Float, default=0.0)

class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    remaining_amount = Column(Float, default=0.0)
    interest_rate = Column(Float, default=0.0)
    emi = Column(Float, default=0.0)
    extra_payment = Column(Float, default=0.0)
    due_date = Column(Integer) # Day of the month

class CreditCard(Base):
    __tablename__ = "credit_cards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    limit = Column(Float, default=0.0)
    used_amount = Column(Float, default=0.0)
    interest_rate = Column(Float, default=0.0)
    minimum_due = Column(Float, default=0.0)
    billing_date = Column(Integer) # Day of the month
    due_date = Column(Integer) # Day of the month
