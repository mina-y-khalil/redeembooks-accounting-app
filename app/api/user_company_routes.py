from flask import Blueprint, request
from flask_login import login_required, current_user
from app.models import db, UserCompany, User
from datetime import datetime

user_company_routes = Blueprint('user_companies', __name__)

def check_access(company_id):  # Added helper
    return UserCompany.query.filter_by(user_id=current_user.id, company_id=company_id).first()



# Get all users for a company
@user_company_routes.route('/companies/<int:company_id>/users', methods=['GET'])
@login_required
def get_users_for_company(company_id):

    if not check_access(company_id):  # Access check
        return {"errors": ["Unauthorized"]}, 403


    users = UserCompany.query.filter_by(company_id=company_id).all()
    return {"users": [uc.to_dict() for uc in users]}, 200

# Add a user to a company
@user_company_routes.route('/companies/<int:company_id>/users', methods=['POST'])
@login_required
def add_user_to_company(company_id):

    if not check_access(company_id):  # Access check
        return {"errors": ["Unauthorized"]}, 403

    data = request.get_json()
    user = User.query.get(data.get('user_id'))
    if not user:
        return {"errors": ["User not found"]}, 404

    new_uc = UserCompany(
        user_id=user.id,
        company_id=company_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.session.add(new_uc)
    db.session.commit()
    return new_uc.to_dict(), 201

# Remove a user from a company
@user_company_routes.route('/companies/<int:company_id>/users/<int:user_id>', methods=['DELETE'])
@login_required
def remove_user_from_company(company_id, user_id):
    if not check_access(company_id):  # Access check
        return {"errors": ["Unauthorized"]}, 403

    uc = UserCompany.query.filter_by(company_id=company_id, user_id=user_id).first()
    if not uc:
        return {"errors": ["User not found in this company"]}, 404

    db.session.delete(uc)
    db.session.commit()
    return {"message": "User removed from company"}, 200
