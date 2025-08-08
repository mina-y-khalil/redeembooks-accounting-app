from app.models import db, Payment, environment, SCHEMA
from datetime import datetime, date
from sqlalchemy.sql import text

def seed_payments():
    payments = [
        Payment(company_id=1, invoice_id=1, vendor_id=1, user_id=1, payment_date=date(2025, 8, 5), amount=500.00, method="ACH", reference_number="PAY-001", notes="Partial payment for laptops"),
        Payment(company_id=1, invoice_id=2, vendor_id=2, user_id=2, payment_date=date(2025, 8, 3), amount=300.00, method="Check", reference_number="PAY-002", notes="Full stationery payment"),
        Payment(company_id=2, invoice_id=3, vendor_id=3, user_id=3, payment_date=date(2025, 8, 7), amount=1000.00, method="Wire", reference_number="PAY-003", notes="First installment for legal fees"),
        Payment(company_id=3, invoice_id=4, vendor_id=4, user_id=4, payment_date=date(2025, 8, 2), amount=500.00, method="ACH", reference_number="PAY-004", notes="Paid food ingredients")
    ]
    db.session.add_all(payments)
    db.session.commit()

def undo_payments():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.payments RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM payments"))
    db.session.commit()
