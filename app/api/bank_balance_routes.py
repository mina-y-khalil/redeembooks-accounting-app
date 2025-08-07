from flask import Blueprint, request
from flask_login import login_required, current_user
from app.models import db, BankBalance, UserCompany
from datetime import datetime

bank_balance_routes = Blueprint('bank_balances', __name__)

def check_access(company_id):
    return UserCompany.query.filter_by(user_id=current_user.id, company_id=company_id).first()

# GET all balances
@bank_balance_routes.route('/companies/<int:company_id>/balances', methods=['GET'])
@login_required
def get_balances(company_id):
    if not check_access(company_id):
        return {"errors": ["Unauthorized"]}, 403
    balances = BankBalance.query.filter_by(company_id=company_id).all()
    return {"balances": [b.to_dict() for b in balances]}, 200

# POST a new balance
@bank_balance_routes.route('/companies/<int:company_id>/balances', methods=['POST'])
@login_required
def create_balance(company_id):
    if not check_access(company_id):
        return {"errors": ["Unauthorized"]}, 403

    data = request.get_json()
    balance = BankBalance(
        company_id=company_id,
        balance=data.get('balance'),
        effective_date=datetime.strptime(data.get('effective_date'), "%Y-%m-%d").date()
    )
    db.session.add(balance)
    db.session.commit()
    return balance.to_dict(), 201

# PUT update balance
@bank_balance_routes.route('/balances/<int:id>', methods=['PUT'])
@login_required
def update_balance(id):
    balance = BankBalance.query.get(id)
    if not balance:
        return {"errors": ["Balance not found"]}, 404

    if not check_access(balance.company_id):
        return {"errors": ["Unauthorized"]}, 403

    data = request.get_json()
    balance.balance = data.get('balance')
    balance.effective_date = datetime.strptime(data.get('effective_date'), "%Y-%m-%d").date()
    db.session.commit()
    return balance.to_dict(), 200

# DELETE balance
@bank_balance_routes.route('/balances/<int:id>', methods=['DELETE'])
@login_required
def delete_balance(id):
    balance = BankBalance.query.get(id)
    if not balance:
        return {"errors": ["Balance not found"]}, 404

    if not check_access(balance.company_id):
        return {"errors": ["Unauthorized"]}, 403

    db.session.delete(balance)
    db.session.commit()
    return {"message": "Deleted"}, 200
