from flask import Blueprint
from flask_login import login_required, current_user
from app.models import db, AuditLog, UserCompany

audit_log_routes = Blueprint('audit_logs', __name__)

@audit_log_routes.route('/companies/<int:company_id>/audit-logs', methods=['GET'])
@login_required
def get_audit_logs(company_id):
    # Access check
    access = UserCompany.query.filter_by(user_id=current_user.id, company_id=company_id).first()
    if not access:
        return {"errors": ["Unauthorized: You don't have access to this company"]}, 403

    logs = AuditLog.query.filter_by(company_id=company_id).order_by(AuditLog.created_at.desc()).all()
    return {"audit_logs": [log.to_dict() for log in logs]}, 200
