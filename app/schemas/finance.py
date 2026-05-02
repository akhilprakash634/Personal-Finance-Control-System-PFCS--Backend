from pydantic import BaseModel
from typing import List, Optional

# --- Account Schemas ---
class AccountBase(BaseModel):
    name: str
    type: str
    balance: float

class AccountCreate(AccountBase):
    pass

class Account(AccountBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True

# --- Loan Schemas ---
class LoanBase(BaseModel):
    name: str
    remaining_amount: float
    interest_rate: float
    emi: float
    extra_payment: float
    due_date: int

class LoanCreate(LoanBase):
    pass

class Loan(LoanBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True

# --- CreditCard Schemas ---
class CreditCardBase(BaseModel):
    name: str
    limit: float
    used_amount: float
    interest_rate: float
    minimum_due: float
    billing_date: int
    due_date: int

class CreditCardCreate(CreditCardBase):
    pass

class CreditCard(CreditCardBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True

# --- Engine Output Schemas ---
class DebtItem(BaseModel):
    name: str
    type: str
    balance: float
    interest: float
    min_payment: float

class Summary(BaseModel):
    total_balance: float
    total_debt: float
    net_worth: float

class MonthlyRequirement(BaseModel):
    total_required: float
    loan_emi_total: float
    credit_min_due_total: float

class StrategyStep(BaseModel):
    focus: str
    reason: str
    steps: List[str]

class DashboardResponse(BaseModel):
    summary: Summary
    monthly_requirement: MonthlyRequirement
    strategy: StrategyStep
    alerts: List[str]
