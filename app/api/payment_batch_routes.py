from flask import Blueprint, request
from flask_login import login_required, current_user
from app.models import db, PaymentBatch
from datetime import datetime


payment_batch_routes = Blueprint('payment_batches', __name__)

# Get All Batches for a Company
@payment_batch_routes.route('/companies/<int:company_id>/batches', methods=['GET'])
@login_required
def get_batches(company_id):
    batches = PaymentBatch.query.filter_by(company_id=company_id).all()
    return {"batches": [batch.to_dict() for batch in batches]}, 200

# Get Batch by ID
@payment_batch_routes.route('/batches/<int:id>', methods=['GET'])
@login_required
def get_batch(id):
    batch = PaymentBatch.query.get(id)
    if not batch:
        return {"errors": ["Batch not found"]}, 404
    return batch.to_dict(), 200

# Create Batch
@payment_batch_routes.route('/companies/<int:company_id>/batches', methods=['POST'])
@login_required
def create_batch(company_id):
    data = request.get_json()

    batch_date = datetime.strptime(data.get('batch_date'), '%Y-%m-%d').date()
    scheduled_for = datetime.strptime(data.get('scheduled_for'), '%Y-%m-%d').date()

    batch = PaymentBatch(
        company_id=company_id,
        user_id=current_user.id,
        batch_date=batch_date,
        total_amount=data.get('total_amount'),
        scheduled_for=scheduled_for,
        status=data.get('status', 'scheduled')
    )
    db.session.add(batch)
    db.session.commit()
    return batch.to_dict(), 201

# Update Batch
@payment_batch_routes.route('/batches/<int:id>', methods=['PUT'])
@login_required
def update_batch(id):
    batch = PaymentBatch.query.get(id)
    if not batch:
        return {"errors": ["Batch not found"]}, 404

    data = request.get_json()

    if 'batch_date' in data:
        batch.batch_date = datetime.strptime(data['batch_date'], '%Y-%m-%d').date()
    if 'scheduled_for' in data:
        batch.scheduled_for = datetime.strptime(data['scheduled_for'], '%Y-%m-%d').date()
    if 'total_amount' in data:
        batch.total_amount = data['total_amount']
    if 'status' in data:
        batch.status = data['status']

    db.session.commit()
    return batch.to_dict(), 200


# Delete Batch
@payment_batch_routes.route('/batches/<int:id>', methods=['DELETE'])
@login_required
def delete_batch(id):
    batch = PaymentBatch.query.get(id)
    if not batch:
        return {"errors": ["Batch not found"]}, 404
    
    db.session.delete(batch)
    db.session.commit()
    return {"message": "Successfully deleted"}, 200
