from app.models import db, Category, environment, SCHEMA
from datetime import datetime
from sqlalchemy.sql import text

def seed_categories():
    categories = [
        Category(company_id=1, name="Office Supplies", description="Stationery and general office items"),
        Category(company_id=1, name="Technology", description="Hardware, software, and IT services"),
        Category(company_id=2, name="Legal Services", description="Lawyer and contract fees"),
        Category(company_id=3, name="Food Ingredients", description="Groceries and raw materials for restaurants")
    ]
    db.session.add_all(categories)
    db.session.commit()

def undo_categories():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.categories RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM categories"))
    db.session.commit()
