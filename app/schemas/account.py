from pydantic import BaseModel

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
