from pydantic import BaseModel

class CreditCardBase(BaseModel):
    name: str
    limit: float
    used_amount: float
    available_limit: float
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
