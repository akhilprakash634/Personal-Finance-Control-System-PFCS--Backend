from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.finance import Loan
from app.schemas.finance import Loan as LoanSchema, LoanCreate

router = APIRouter(prefix="/loans", tags=["loans"])

@router.get("/", response_model=List[LoanSchema])
def get_loans(db: Session = Depends(get_db)):
    return db.query(Loan).all()

@router.post("/", response_model=LoanSchema)
def create_loan(loan: LoanCreate, db: Session = Depends(get_db)):
    db_loan = Loan(**loan.dict())
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan
