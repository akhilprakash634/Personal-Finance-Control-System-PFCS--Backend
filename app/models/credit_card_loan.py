from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class CreditCardLoan(Base):
    __tablename__ = "credit_card_loans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    card_id = Column(Integer, ForeignKey("credit_cards.id"), nullable=False)
    name = Column(String, index=True) # e.g., "Flipkart PayLater", "Amazon EMI"
    principal = Column(Float, default=0.0)
    remaining_amount = Column(Float, default=0.0)
    interest_rate = Column(Float, default=0.0)
    interest_type = Column(String, default="yearly") # "yearly" or "monthly"
    emi = Column(Float, default=0.0)
    tenure_months = Column(Integer, default=0)
    emis_paid = Column(Integer, default=0)
    status = Column(String, default="active") # "active" or "closed"
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")
    card = relationship("CreditCard", back_populates="loans")
