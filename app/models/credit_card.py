from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class CreditCard(Base):
    __tablename__ = "credit_cards"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, index=True)
    limit = Column(Float, default=0.0)
    used_amount = Column(Float, default=0.0)
    available_limit = Column(Float, default=0.0)
    current_month_bill = Column(Float, default=0.0)
    interest_rate = Column(Float, default=0.0)
    minimum_due = Column(Float, default=0.0)
    billing_date = Column(Integer) # Day of the month
    due_date = Column(Integer) # Day of the month

    user = relationship("User")
    loans = relationship("CreditCardLoan", back_populates="card")
