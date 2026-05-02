from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.finance import CreditCard
from app.schemas.finance import CreditCard as CreditCardSchema, CreditCardCreate

router = APIRouter(prefix="/credit-cards", tags=["credit_cards"])

@router.get("/", response_model=List[CreditCardSchema])
def get_credit_cards(db: Session = Depends(get_db)):
    return db.query(CreditCard).all()

@router.post("/", response_model=CreditCardSchema)
def create_credit_card(card: CreditCardCreate, db: Session = Depends(get_db)):
    db_card = CreditCard(**card.dict())
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card
