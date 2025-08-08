from app.models import db, User, Company, UserCompany, environment, SCHEMA
from sqlalchemy.sql import text
from datetime import datetime


# Adds a demo user, you can add other users here if you want
def seed_users():
    users = [
        User(username="owner1", email="owner1@example.com", password="password", role="Owner"),
        User(username="manager1", email="manager1@example.com", password="password", role="Manager"),
        User(username="staff1", email="staff1@example.com", password="password", role="Staff"),
        User(username="demo_user", email="demo@example.com", password="password", role="Owner")
    ]


    db.session.add_all(users)
    db.session.commit()

    # 🔥 Create a demo company
    demo_company = Company(
        name="Demo Company",
        tax_id="11-1111111",
        street="123 Demo St",
        city="San Ramon",
        county="Contra Costa",
        state="CA",
        zipcode="94582",
        phone="925-555-0000",
        email="demo@company.com",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.session.add(demo_company)
    db.session.commit()

    # 🔥 Link demo user to demo company
    demo_user = User.query.filter_by(email="demo@example.com").first()
    demo_link = UserCompany(
        user_id=demo_user.id,
        company_id=demo_company.id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.session.add(demo_link)
    db.session.commit()




# Uses a raw SQL query to TRUNCATE or DELETE the users table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_users():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.user_companies RESTART IDENTITY CASCADE;")
        db.session.execute(f"TRUNCATE table {SCHEMA}.companies RESTART IDENTITY CASCADE;")
        db.session.execute(f"TRUNCATE table {SCHEMA}.users RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM user_companies"))
        db.session.execute(text("DELETE FROM companies"))
        db.session.execute(text("DELETE FROM users"))
        
    db.session.commit()
