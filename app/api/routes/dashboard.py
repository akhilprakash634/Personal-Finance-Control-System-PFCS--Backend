from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.account import Account
from app.models.loan import Loan
from app.models.credit_card import CreditCard
from app.models.payment import Payment
from app.models.user import User
from pydantic import BaseModel
from app.services.finance_engine import create_dashboard
from app.core.security import get_current_user

class Summary(BaseModel):
    total_balance: float
    total_debt: float
    net_worth: float

class MonthlyRequirement(BaseModel):
    total_required: float
    loan_emi_total: float
    credit_min_due_total: float

class StrategyStep(BaseModel):
    focus: str
    reason: str
    steps: List[str]

class ThisMonth(BaseModel):
    total_paid: float
    interest_paid: float
    principal_reduced: float
    insights: List[str]

class DashboardResponse(BaseModel):
    summary: Summary
    monthly_requirement: MonthlyRequirement
    strategy: StrategyStep
    alerts: List[str]
    this_month: ThisMonth

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/", response_model=DashboardResponse)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    accounts = db.query(Account).filter(Account.user_id == current_user.id).all()
    loans = db.query(Loan).filter(Loan.user_id == current_user.id).all()
    credit_cards = db.query(CreditCard).filter(CreditCard.user_id == current_user.id).all()
    payments = db.query(Payment).filter(Payment.user_id == current_user.id).all()
    
    dashboard_data = create_dashboard(accounts, loans, credit_cards, payments)
    return dashboard_data
