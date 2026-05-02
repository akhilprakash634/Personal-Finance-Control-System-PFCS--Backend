from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.db.session import get_db
from app.models.payment import Payment
from app.models.loan import Loan
from app.models.credit_card import CreditCard
from app.models.user import User
from app.schemas.payment import Payment as PaymentSchema, PaymentCreate
from app.services.finance_engine import calculate_payment_split
from app.core.security import get_current_user

router = APIRouter(prefix="/payments", tags=["payments"])

@router.get("/", response_model=List[PaymentSchema])
def get_payments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Payment).filter(Payment.user_id == current_user.id).all()

@router.post("/", response_model=PaymentSchema)
def create_payment(
    payment: PaymentCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. Fetch the debt object (ensure it belongs to the user)
    debt = None
    if payment.debt_type == "loan":
        debt = db.query(Loan).filter(Loan.id == payment.debt_id, Loan.user_id == current_user.id).first()
    elif payment.debt_type == "credit_card":
        debt = db.query(CreditCard).filter(CreditCard.id == payment.debt_id, CreditCard.user_id == current_user.id).first()
    
    if not debt:
        raise HTTPException(status_code=404, detail=f"{payment.debt_type} not found or access denied")

    # 2. Calculate interest/principal split
    split = calculate_payment_split(payment.debt_type, debt, payment.amount)
    
    # 3. Update the debt balance
    if payment.debt_type == "loan":
        debt.remaining_amount -= split["principal"]
        if debt.remaining_amount <= 0:
            debt.remaining_amount = 0
            debt.status = "closed"
            debt.closed_date = datetime.now()
    else: # credit_card
        debt.used_amount -= split["principal"]
        if debt.used_amount < 0:
            debt.used_amount = 0

    # 4. Create the payment record
    db_payment = Payment(
        user_id=current_user.id,
        debt_type=payment.debt_type,
        debt_id=payment.debt_id,
        amount=payment.amount,
        payment_type=payment.payment_type,
        interest_component=split["interest"],
        principal_component=split["principal"]
    )
    
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment
