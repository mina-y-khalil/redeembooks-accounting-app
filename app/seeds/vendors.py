from app.models import db, Vendor, environment, SCHEMA
from datetime import datetime
from sqlalchemy.sql import text

def seed_vendors():
    vendors = [
        Vendor(company_id=1, name="Tech Supplies Inc", contact_name="Alice Johnson", email="alice@techsupplies.com", phone="415-987-6543", tax_id="99-1122334", street="55 Silicon Rd", city="San Francisco", county="SF", state="CA", zipcode="94107", preferred_payment_method="ACH", payment_terms="Net 30"),
        Vendor(company_id=1, name="Office Essentials", contact_name="Bob Smith", email="bob@officeessentials.com", phone="415-456-7890", tax_id="88-2233445", street="88 Paper Lane", city="San Francisco", county="SF", state="CA", zipcode="94108", preferred_payment_method="Check", payment_terms="Net 15"),
        Vendor(company_id=2, name="Real Estate Law Group", contact_name="Carol White", email="carol@relawgroup.com", phone="408-555-8989", tax_id="77-3344556", street="200 Legal Blvd", city="San Jose", county="Santa Clara", state="CA", zipcode="95112", preferred_payment_method="Wire", payment_terms="Net 45"),
        Vendor(company_id=3, name="Food Distribution LLC", contact_name="Dan Brown", email="dan@fooddist.com", phone="323-666-1212", tax_id="66-4455667", street="300 Gourmet St", city="Los Angeles", county="LA", state="CA", zipcode="90002", preferred_payment_method="ACH", payment_terms="Net 30")
    ]
    db.session.add_all(vendors)
    db.session.commit()

def undo_vendors():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.vendors RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM vendors"))
    db.session.commit()
