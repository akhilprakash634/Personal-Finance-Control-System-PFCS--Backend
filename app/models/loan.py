from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, index=True)
    remaining_amount = Column(Float, default=0.0)
    interest_rate = Column(Float, default=0.0)
    interest_type = Column(String, default="yearly") # "yearly" or "monthly"
    loan_category = Column(String, default="personal") # "personal", "credit_card_loan", "paylater"
    emi = Column(Float, default=0.0)
    extra_payment = Column(Float, default=0.0)
    tenure = Column(Integer, default=0) # Total months
    emis_paid = Column(Integer, default=0) # EMIs paid so far
    due_date = Column(Integer) # Day of the month
    status = Column(String, default="active") # "active" or "closed"
    closed_date = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User")
