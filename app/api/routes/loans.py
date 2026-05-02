from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.loan import Loan
from app.models.user import User
from app.schemas.loan import Loan as LoanSchema, LoanCreate
from app.core.security import get_current_user

router = APIRouter(prefix="/loans", tags=["loans"])

@router.get("/", response_model=List[LoanSchema])
def get_loans(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Loan).filter(Loan.user_id == current_user.id).all()

@router.post("/", response_model=LoanSchema)
def create_loan(
    loan: LoanCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_loan = Loan(**loan.dict(), user_id=current_user.id)
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan
