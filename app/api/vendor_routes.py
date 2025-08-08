from flask import Blueprint, request
from flask_login import login_required, current_user
from app.models import db, Vendor, UserCompany

vendor_routes = Blueprint('vendors', __name__)

def check_access(company_id):  # Added helper
    return UserCompany.query.filter_by(user_id=current_user.id, company_id=company_id).first()



# Get All Vendors
@vendor_routes.route('/companies/<int:company_id>/vendors', methods=['GET'])
@login_required
def get_vendors(company_id):

    if not check_access(company_id):  # Access check
        return {"errors": ["Unauthorized"]}, 403

    vendors = Vendor.query.filter_by(company_id=company_id).all()
    return {"vendors": [vendor.to_dict() for vendor in vendors]}, 200

# Get Vendor by ID
@vendor_routes.route('/vendors/<int:id>', methods=['GET'])
@login_required
def get_vendor(id):
    vendor = Vendor.query.get(id)
    if not vendor:
        return {"errors": ["Vendor not found"]}, 404
    
    if not check_access(vendor.company_id):  # Access check
        return {"errors": ["Unauthorized"]}, 403

    return vendor.to_dict(), 200

# Create Vendor
@vendor_routes.route('/companies/<int:company_id>/vendors', methods=['POST'])
@login_required
def create_vendor(company_id):
    if not check_access(company_id):  # Access check
        return {"errors": ["Unauthorized"]}, 403


    data = request.get_json()
    vendor = Vendor(
        company_id=company_id,
        name=data.get('name'),
        contact_name=data.get('contact_name'),
        email=data.get('email'),
        phone=data.get('phone'),
        tax_id=data.get('tax_id'),
        street=data.get('street'),
        city=data.get('city'),
        county=data.get('county'),
        state=data.get('state'),
        zipcode=data.get('zipcode'),
        preferred_payment_method=data.get('preferred_payment_method'),
        payment_terms=data.get('payment_terms'),
        w9_document_url=data.get('w9_document_url')
    )
    db.session.add(vendor)
    db.session.commit()
    return vendor.to_dict(), 201

# Update Vendor
@vendor_routes.route('/vendors/<int:id>', methods=['PUT'])
@login_required
def update_vendor(id):
    vendor = Vendor.query.get(id)
    if not vendor:
        return {"errors": ["Vendor not found"]}, 404
    
    if not check_access(vendor.company_id):  # Access check
        return {"errors": ["Unauthorized"]}, 403

    
    data = request.get_json()
    for field in ['name', 'contact_name', 'email', 'phone', 'tax_id', 'street', 
                  'city', 'county', 'state', 'zipcode', 'preferred_payment_method', 
                  'payment_terms', 'w9_document_url']:
        if field in data:
            setattr(vendor, field, data[field])
    
    db.session.commit()
    return vendor.to_dict(), 200

# Delete Vendor
@vendor_routes.route('/vendors/<int:id>', methods=['DELETE'])
@login_required
def delete_vendor(id):
    vendor = Vendor.query.get(id)
    if not vendor:
        return {"errors": ["Vendor not found"]}, 404
    
    if not check_access(vendor.company_id):  # Access check
        return {"errors": ["Unauthorized"]}, 403
    
    db.session.delete(vendor)
    db.session.commit()
    return {"message": "Successfully deleted"}, 200
