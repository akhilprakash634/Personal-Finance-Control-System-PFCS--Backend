from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.credit_card import CreditCard
from app.models.user import User
from app.schemas.credit_card import CreditCard as CreditCardSchema, CreditCardCreate
from app.core.security import get_current_user

router = APIRouter(prefix="/credit-cards", tags=["credit-cards"])

@router.get("/", response_model=List[CreditCardSchema])
def get_credit_cards(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(CreditCard).filter(CreditCard.user_id == current_user.id).all()

@router.post("/", response_model=CreditCardSchema)
def create_credit_card(
    card: CreditCardCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_card = CreditCard(**card.dict(), user_id=current_user.id)
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card
