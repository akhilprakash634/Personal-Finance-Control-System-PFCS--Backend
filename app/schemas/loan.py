from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LoanBase(BaseModel):
    name: str
    remaining_amount: float
    interest_rate: float
    interest_type: str = "yearly"
    loan_category: str = "personal"
    emi: float
    extra_payment: float
    tenure: int
    emis_paid: int
    due_date: int
    status: str = "active"
    closed_date: Optional[datetime] = None

class LoanCreate(LoanBase):
    pass

class Loan(LoanBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True
