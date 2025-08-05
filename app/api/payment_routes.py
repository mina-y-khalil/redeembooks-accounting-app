from flask import Blueprint, request
from flask_login import login_required, current_user
from app.models import db, Payment
from datetime import datetime


payment_routes = Blueprint('payments', __name__)

# Get All Payments for a Company
@payment_routes.route('/companies/<int:company_id>/payments', methods=['GET'])
@login_required
def get_payments(company_id):
    payments = Payment.query.filter_by(company_id=company_id).all()
    return {"payments": [payment.to_dict() for payment in payments]}, 200

# Get Payment by ID
@payment_routes.route('/payments/<int:id>', methods=['GET'])
@login_required
def get_payment(id):
    payment = Payment.query.get(id)
    if not payment:
        return {"errors": ["Payment not found"]}, 404
    return payment.to_dict(), 200

# Create Payment
@payment_routes.route('/companies/<int:company_id>/payments', methods=['POST'])
@login_required
def create_payment(company_id):
    data = request.get_json()

    try:
        payment_date = datetime.strptime(data.get('payment_date'), '%Y-%m-%d').date()
    except Exception:
        return {"errors": ["Invalid date format. Use YYYY-MM-DD"]}, 400


    payment = Payment(
        company_id=company_id,
        invoice_id=data.get('invoice_id'),
        vendor_id=data.get('vendor_id'),
        user_id=current_user.id,
        payment_date=payment_date,
        amount=data.get('amount'),
        method=data.get('method'),
        reference_number=data.get('reference_number'),
        notes=data.get('notes'),
        batch_id=data.get('batch_id')
    )
    db.session.add(payment)
    db.session.commit()
    return payment.to_dict(), 201

# Update Payment
@payment_routes.route('/payments/<int:id>', methods=['PUT'])
@login_required
def update_payment(id):
    payment = Payment.query.get(id)
    if not payment:
        return {"errors": ["Payment not found"]}, 404

    data = request.get_json()
    for field in [
        'invoice_id', 'vendor_id', 'payment_date', 
        'amount', 'method', 'reference_number', 'notes', 'batch_id'
    ]:
        if field in data:
            setattr(payment, field, data[field])

    db.session.commit()
    return payment.to_dict(), 200

# Delete Payment
@payment_routes.route('/payments/<int:id>', methods=['DELETE'])
@login_required
def delete_payment(id):
    payment = Payment.query.get(id)
    if not payment:
        return {"errors": ["Payment not found"]}, 404
    
    db.session.delete(payment)
    db.session.commit()
    return {"message": "Successfully deleted"}, 200
