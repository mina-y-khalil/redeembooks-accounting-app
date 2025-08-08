from app.models import db, BankBalance, environment, SCHEMA
from datetime import datetime, date
from sqlalchemy.sql import text

def seed_bank_balances():
    balances = [
        BankBalance(company_id=1, balance=5000.00, effective_date=date(2025, 8, 1)),
        BankBalance(company_id=2, balance=7000.00, effective_date=date(2025, 8, 1)),
        BankBalance(company_id=3, balance=3000.00, effective_date=date(2025, 8, 1)),
        BankBalance(company_id=4, balance=10000.00, effective_date=date(2025, 8, 1))
    ]
    db.session.add_all(balances)
    db.session.commit()

def undo_bank_balances():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.bank_balances RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM bank_balances"))
    db.session.commit()
