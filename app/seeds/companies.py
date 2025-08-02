from app.models import db, Company, environment, SCHEMA
from datetime import datetime
from sqlalchemy.sql import text

def seed_companies():
    companies = [
        Company(name="Redeem Innovations LLC", tax_id="98-7654321", street="123 Tech Ave", city="San Francisco", county="SF", state="CA", zipcode="94105", phone="415-123-4567", email="info@redeeminnovations.com"),
        Company(name="Redeem Real Estate", tax_id="12-3456789", street="500 Market St", city="San Jose", county="Santa Clara", state="CA", zipcode="95113", phone="408-555-1212", email="contact@redeemrealestate.com"),
        Company(name="Redeem Restaurants", tax_id="22-3344556", street="78 Culinary Blvd", city="Los Angeles", county="LA", state="CA", zipcode="90001", phone="323-789-6543", email="hello@redeemrestaurants.com"),
        Company(name="Redeem Financial Services", tax_id="11-2233445", street="100 Finance St", city="San Diego", county="SD", state="CA", zipcode="92101", phone="619-321-9876", email="support@redeemfinance.com")
    ]
    db.session.add_all(companies)
    db.session.commit()

def undo_companies():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.companies RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM companies"))
    db.session.commit()
