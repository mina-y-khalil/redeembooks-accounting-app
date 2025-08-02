from app.models import db, AuditLog, environment, SCHEMA
from datetime import datetime
from sqlalchemy.sql import text

def seed_audit_logs():
    logs = [
        AuditLog(user_id=1, company_id=1, action="CREATE", table_name="invoices", record_id=1, old_data=None, new_data="{'amount': 1500}", created_at=datetime.utcnow()),
        AuditLog(user_id=2, company_id=1, action="APPROVE", table_name="invoices", record_id=2, old_data="{'status': 'pending'}", new_data="{'status': 'approved'}", created_at=datetime.utcnow()),
        AuditLog(user_id=3, company_id=2, action="UPDATE", table_name="vendors", record_id=3, old_data="{'phone': '408-555-1212'}", new_data="{'phone': '408-999-1212'}", created_at=datetime.utcnow()),
        AuditLog(user_id=4, company_id=3, action="DELETE", table_name="categories", record_id=4, old_data="{'name': 'Food Ingredients'}", new_data=None, created_at=datetime.utcnow())
    ]
    db.session.add_all(logs)
    db.session.commit()

def undo_audit_logs():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.audit_logs RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM audit_logs"))
    db.session.commit()
