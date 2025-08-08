from flask import Blueprint, request
from flask_login import login_required, current_user
from app.models import db, Approver, UserCompany, User
from datetime import datetime

approver_routes = Blueprint('approvers', __name__)

# Get all approvers for a company (with access check)
@approver_routes.route('/companies/<int:company_id>/approvers', methods=['GET'])
@login_required
def get_approvers(company_id):
    user_company = UserCompany.query.filter_by(
        user_id=current_user.id,
        company_id=company_id
    ).first()
    if not user_company:
        return {"errors": ["Unauthorized: You don't have access to this company"]}, 403

    approvers = Approver.query.filter_by(company_id=company_id).all()
    return {"approvers": [approver.to_dict() for approver in approvers]}, 200


# Get a single approver (with access check)
@approver_routes.route('/approvers/<int:id>', methods=['GET'])
@login_required
def get_approver(id):
    approver = Approver.query.get(id)
    if not approver:
        return {"errors": ["Approver not found"]}, 404

    user_company = UserCompany.query.filter_by(
        user_id=current_user.id,
        company_id=approver.company_id
    ).first()
    if not user_company:
        return {"errors": ["Unauthorized: You don't have access to this company"]}, 403

    return approver.to_dict(), 200


# Create approver
@approver_routes.route('/companies/<int:company_id>/approvers', methods=['POST'])
@login_required
def create_approver(company_id):
    user_company = UserCompany.query.filter_by(
        user_id=current_user.id,
        company_id=company_id
    ).first()
    if not user_company:
        return {"errors": ["Unauthorized: You don't have access to this company"]}, 403

    data = request.get_json()
    user = User.query.get(data.get('user_id'))
    if not user:
        return {"errors": ["User not found"]}, 404

    approver = Approver(
        user_id=user.id,
        company_id=company_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.session.add(approver)
    db.session.commit()
    return approver.to_dict(), 201


# Update approver
@approver_routes.route('/approvers/<int:id>', methods=['PUT'])
@login_required
def update_approver(id):
    approver = Approver.query.get(id)
    if not approver:
        return {"errors": ["Approver not found"]}, 404

    user_company = UserCompany.query.filter_by(
        user_id=current_user.id,
        company_id=approver.company_id
    ).first()
    if not user_company:
        return {"errors": ["Unauthorized: You don't have access to this company"]}, 403

    data = request.get_json()
    if 'user_id' in data:
        user = User.query.get(data['user_id'])
        if not user:
            return {"errors": ["User not found"]}, 404
        approver.user_id = data['user_id']

    approver.updated_at = datetime.utcnow()
    db.session.commit()
    return approver.to_dict(), 200


# Delete approver
@approver_routes.route('/approvers/<int:id>', methods=['DELETE'])
@login_required
def delete_approver(id):
    approver = Approver.query.get(id)
    if not approver:
        return {"errors": ["Approver not found"]}, 404

    user_company = UserCompany.query.filter_by(
        user_id=current_user.id,
        company_id=approver.company_id
    ).first()
    if not user_company:
        return {"errors": ["Unauthorized: You don't have access to this company"]}, 403

    db.session.delete(approver)
    db.session.commit()
    return {"message": "Successfully deleted"}, 200
