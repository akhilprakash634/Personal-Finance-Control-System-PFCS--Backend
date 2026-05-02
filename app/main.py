from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import accounts, loans, credit_cards, dashboard
from app.db.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Personal Finance Management System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(accounts.router)
app.include_router(loans.router)
app.include_router(credit_cards.router)
app.include_router(dashboard.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to PFCS API"}
