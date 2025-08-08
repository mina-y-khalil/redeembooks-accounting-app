from app.models import db, Invoice, environment, SCHEMA
from datetime import datetime, date
from sqlalchemy.sql import text

def seed_invoices():
    invoices = [
        Invoice(company_id=1, vendor_id=1, user_id=1, category_id=2, invoice_number="INV-1001", invoice_date=date(2025, 8, 1), voucher_date=date(2025, 8, 2), due_date=date(2025, 8, 15), amount=1500.00, status="pending", description="Purchase of new laptops"),
        Invoice(company_id=1, vendor_id=2, user_id=2, category_id=1, invoice_number="INV-1002", invoice_date=date(2025, 7, 25), voucher_date=date(2025, 7, 26), due_date=date(2025, 8, 5), amount=300.00, status="approved", description="Stationery order"),
        Invoice(company_id=2, vendor_id=3, user_id=3, category_id=3, invoice_number="INV-2001", invoice_date=date(2025, 8, 1), voucher_date=date(2025, 8, 1), due_date=date(2025, 8, 20), amount=2000.00, status="pending", description="Real estate legal fees"),
        Invoice(company_id=3, vendor_id=4, user_id=4, category_id=4, invoice_number="INV-3001", invoice_date=date(2025, 7, 28), voucher_date=date(2025, 7, 29), due_date=date(2025, 8, 10), amount=500.00, status="paid", description="Bulk food ingredients")
    ]
    db.session.add_all(invoices)
    db.session.commit()

def undo_invoices():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.invoices RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM invoices"))
    db.session.commit()
