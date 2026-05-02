from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.finance import Account, Loan, CreditCard
from app.schemas.finance import DashboardResponse
from app.services.finance_engine import create_dashboard

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/", response_model=DashboardResponse)
def get_dashboard(db: Session = Depends(get_db)):
    accounts = db.query(Account).all()
    loans = db.query(Loan).all()
    credit_cards = db.query(CreditCard).all()
    
    dashboard_data = create_dashboard(accounts, loans, credit_cards)
    return dashboard_data
