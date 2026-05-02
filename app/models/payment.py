from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    debt_type = Column(String)  # "loan" or "credit_card"
    debt_id = Column(Integer)   # ID of the loan or card
    amount = Column(Float)
    payment_type = Column(String)  # "emi", "extra", "minimum"
    interest_component = Column(Float, default=0.0)
    principal_component = Column(Float, default=0.0)
    date = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")
