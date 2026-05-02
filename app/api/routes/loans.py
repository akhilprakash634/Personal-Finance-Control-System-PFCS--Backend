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

@router.put("/{loan_id}", response_model=LoanSchema)
def update_loan(
    loan_id: int,
    loan_update: LoanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_loan = db.query(Loan).filter(Loan.id == loan_id, Loan.user_id == current_user.id).first()
    if not db_loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    
    for key, value in loan_update.dict().items():
        setattr(db_loan, key, value)
    
    db.commit()
    db.refresh(db_loan)
    return db_loan

@router.delete("/{loan_id}")
def delete_loan(
    loan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_loan = db.query(Loan).filter(Loan.id == loan_id, Loan.user_id == current_user.id).first()
    if not db_loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    
    db.delete(db_loan)
    db.commit()
    return {"message": "Loan deleted"}
