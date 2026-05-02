from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class CreditCardLoanBase(BaseModel):
    card_id: int
    name: str
    principal: float
    remaining_amount: float
    interest_rate: float
    interest_type: str = "yearly"
    emi: float
    tenure_months: int
    emis_paid: int = 0
    status: str = "active"

class CreditCardLoanCreate(CreditCardLoanBase):
    pass

class CreditCardLoan(CreditCardLoanBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
