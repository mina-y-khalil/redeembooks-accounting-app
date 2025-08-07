from flask import Blueprint, request
from flask_login import login_required, current_user
from app.models import db, Invoice, UserCompany
from datetime import datetime

invoice_routes = Blueprint('invoices', __name__)

def check_access(company_id):  # Helper for access control
    return UserCompany.query.filter_by(user_id=current_user.id, company_id=company_id).first()



def str_to_date(date_str):
    if date_str:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    return None

# Get All Invoices for a Company
@invoice_routes.route('/companies/<int:company_id>/invoices', methods=['GET'])
@login_required
def get_invoices(company_id):
    if not check_access(company_id):  # Access check
        return {"errors": ["Unauthorized"]}, 403

    invoices = Invoice.query.filter_by(company_id=company_id).all()
    return {"invoices": [invoice.to_dict() for invoice in invoices]}, 200

# Get Invoice by ID
@invoice_routes.route('/invoices/<int:id>', methods=['GET'])
@login_required
def get_invoice(id):
    invoice = Invoice.query.get(id)
    if not invoice:
        return {"errors": ["Invoice not found"]}, 404
    
    if not check_access(invoice.company_id):  # Access check
        return {"errors": ["Unauthorized"]}, 403

    return invoice.to_dict(), 200

# Create Invoice
@invoice_routes.route('/companies/<int:company_id>/invoices', methods=['POST'])
@login_required
def create_invoice(company_id):
    if not check_access(company_id):  # Access check
        return {"errors": ["Unauthorized"]}, 403
    data = request.get_json()
    invoice = Invoice(
        company_id=company_id,
        vendor_id=data.get('vendor_id'),
        user_id=current_user.id,
        category_id=data.get('category_id'),
        invoice_number=data.get('invoice_number'),
        invoice_date=str_to_date(data.get('invoice_date')),
        voucher_date=str_to_date(data.get('voucher_date')),
        due_date=str_to_date(data.get('due_date')),
        amount=data.get('amount'),
        status=data.get('status', 'pending'),
        approved_by=data.get('approved_by'),
        approval_date=str_to_date(data.get('approval_date')),
        description=data.get('description'),
        attachment_url=data.get('attachment_url')
    )
    db.session.add(invoice)
    db.session.commit()
    return invoice.to_dict(), 201

# Update Invoice
@invoice_routes.route('/invoices/<int:id>', methods=['PUT'])
@login_required
def update_invoice(id):
    invoice = Invoice.query.get(id)
    if not invoice:
        return {"errors": ["Invoice not found"]}, 404
    
    if not check_access(invoice.company_id):  # Access check
        return {"errors": ["Unauthorized"]}, 403


    data = request.get_json()
    if 'vendor_id' in data: invoice.vendor_id = data['vendor_id']
    if 'category_id' in data: invoice.category_id = data['category_id']
    if 'invoice_number' in data: invoice.invoice_number = data['invoice_number']
    if 'invoice_date' in data: invoice.invoice_date = str_to_date(data['invoice_date'])
    if 'voucher_date' in data: invoice.voucher_date = str_to_date(data['voucher_date'])
    if 'due_date' in data: invoice.due_date = str_to_date(data['due_date'])
    if 'amount' in data: invoice.amount = data['amount']
    if 'status' in data: invoice.status = data['status']
    if 'approved_by' in data: invoice.approved_by = data['approved_by']
    if 'approval_date' in data: invoice.approval_date = str_to_date(data['approval_date'])
    if 'description' in data: invoice.description = data['description']
    if 'attachment_url' in data: invoice.attachment_url = data['attachment_url']

    db.session.commit()
    return invoice.to_dict(), 200

# Delete Invoice
@invoice_routes.route('/invoices/<int:id>', methods=['DELETE'])
@login_required
def delete_invoice(id):
    invoice = Invoice.query.get(id)
    if not invoice:
        return {"errors": ["Invoice not found"]}, 404
    
    if not check_access(invoice.company_id):  # Access check
        return {"errors": ["Unauthorized"]}, 403

    
    db.session.delete(invoice)
    db.session.commit()
    return {"message": "Successfully deleted"}, 200
