from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.account import Account
from app.models.user import User
from app.schemas.account import Account as AccountSchema, AccountCreate
from app.core.security import get_current_user

router = APIRouter(prefix="/accounts", tags=["accounts"])

@router.get("/", response_model=List[AccountSchema])
def get_accounts(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return db.query(Account).filter(Account.user_id == current_user.id).all()

@router.post("/", response_model=AccountSchema)
def create_account(
    account: AccountCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_account = Account(**account.dict(), user_id=current_user.id)
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

@router.put("/{account_id}", response_model=AccountSchema)
def update_account(
    account_id: int, 
    account: AccountCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_account = db.query(Account).filter(Account.id == account_id, Account.user_id == current_user.id).first()
    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    for var, value in vars(account).items():
        setattr(db_account, var, value) if value is not None else None
        
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account
