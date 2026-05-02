from app.db.session import engine, SessionLocal
from app.db.base import Base
from app.models.account import Account
from app.models.loan import Loan
from app.models.credit_card import CreditCard

def seed():
    # Make sure tables exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Check if empty
    if db.query(Account).count() > 0:
        print("Database already seeded")
        return
        
    print("Seeding database...")
    
    # Add Accounts
    a1 = Account(name="HDFC Savings", type="bank", balance=250000.0)
    a2 = Account(name="Paytm Wallet", type="wallet", balance=1500.0)
    a3 = Account(name="Cash", type="cash", balance=5000.0)
    db.add_all([a1, a2, a3])
    
    # Add Loans
    l1 = Loan(name="Car Loan", remaining_amount=450000.0, interest_rate=8.5, emi=12500.0, extra_payment=2500.0, tenure=60, emis_paid=12, due_date=5)
    l2 = Loan(name="Personal Loan", remaining_amount=120000.0, interest_rate=14.0, emi=5500.0, extra_payment=0.0, tenure=36, emis_paid=6, due_date=10)
    db.add_all([l1, l2])
    
    # Add Credit Cards
    c1 = CreditCard(name="HDFC Millennia", limit=150000.0, used_amount=65000.0, interest_rate=42.0, minimum_due=3250.0, billing_date=15, due_date=5)
    c2 = CreditCard(name="SBI SimplyCLICK", limit=75000.0, used_amount=25000.0, interest_rate=36.0, minimum_due=1250.0, billing_date=20, due_date=10)
    db.add_all([c1, c2])
    
    db.commit()
    print("Seeding complete.")
    
if __name__ == "__main__":
    seed()
