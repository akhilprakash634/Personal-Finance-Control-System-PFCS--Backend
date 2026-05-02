from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PaymentBase(BaseModel):
    debt_type: str
    debt_id: int
    amount: float
    payment_type: str
    interest_component: float = 0.0
    principal_component: float = 0.0

class PaymentCreate(PaymentBase):
    pass

class Payment(PaymentBase):
    id: int
    date: datetime

    class Config:
        from_attributes = True
