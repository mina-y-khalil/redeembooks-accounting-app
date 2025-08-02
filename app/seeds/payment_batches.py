from app.models import db, PaymentBatch, environment, SCHEMA
from datetime import datetime, date
from sqlalchemy.sql import text

def seed_payment_batches():
    batches = [
        PaymentBatch(company_id=1, user_id=1, batch_date=date(2025, 8, 6), total_amount=800.00, scheduled_for=date(2025, 8, 7), status="processed"),
        PaymentBatch(company_id=1, user_id=2, batch_date=date(2025, 8, 8), total_amount=300.00, scheduled_for=date(2025, 8, 9), status="scheduled"),
        PaymentBatch(company_id=2, user_id=3, batch_date=date(2025, 8, 10), total_amount=1000.00, scheduled_for=date(2025, 8, 12), status="scheduled"),
        PaymentBatch(company_id=3, user_id=4, batch_date=date(2025, 8, 4), total_amount=500.00, scheduled_for=date(2025, 8, 5), status="processed")
    ]
    db.session.add_all(batches)
    db.session.commit()

def undo_payment_batches():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.payment_batches RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM payment_batches"))
    db.session.commit()
