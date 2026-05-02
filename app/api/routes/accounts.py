from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.finance import Account
from app.schemas.finance import Account as AccountSchema, AccountCreate

router = APIRouter(prefix="/accounts", tags=["accounts"])

@router.get("/", response_model=List[AccountSchema])
def get_accounts(db: Session = Depends(get_db)):
    return db.query(Account).all()

@router.post("/", response_model=AccountSchema)
def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    db_account = Account(**account.dict())
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

@router.put("/{account_id}", response_model=AccountSchema)
def update_account(account_id: int, account: AccountCreate, db: Session = Depends(get_db)):
    db_account = db.query(Account).filter(Account.id == account_id).first()
    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    for var, value in vars(account).items():
        setattr(db_account, var, value) if value is not None else None
        
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account
