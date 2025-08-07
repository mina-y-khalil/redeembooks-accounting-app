from app.models import db, UserCompany
from datetime import datetime

def seed_user_companies():
    mappings = [
        UserCompany(user_id=1, company_id=1, created_at=datetime.utcnow(), updated_at=datetime.utcnow()),
        UserCompany(user_id=2, company_id=1, created_at=datetime.utcnow(), updated_at=datetime.utcnow()),
        UserCompany(user_id=3, company_id=2, created_at=datetime.utcnow(), updated_at=datetime.utcnow()),
        UserCompany(user_id=4, company_id=3, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    ]
    db.session.add_all(mappings)
    db.session.commit()

def undo_user_companies():
    db.session.execute("DELETE FROM user_companies")
    db.session.commit()
