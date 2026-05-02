from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.credit_card_loan import CreditCardLoan
from app.models.credit_card import CreditCard
from app.schemas.credit_card_loan import CreditCardLoanCreate, CreditCardLoan as CreditCardLoanSchema
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/credit-card-loans", tags=["credit-card-loans"])

@router.get("/", response_model=List[CreditCardLoanSchema])
def get_credit_card_loans(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(CreditCardLoan).filter(CreditCardLoan.user_id == current_user.id).all()

@router.post("/", response_model=CreditCardLoanSchema)
def create_credit_card_loan(
    loan: CreditCardLoanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify card belongs to user
    card = db.query(CreditCard).filter(CreditCard.id == loan.card_id, CreditCard.user_id == current_user.id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Credit card not found")
        
    db_loan = CreditCardLoan(**loan.model_dump(), user_id=current_user.id)
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan
