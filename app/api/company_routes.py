from flask import Blueprint, request
from flask_login import login_required, current_user
from app.models import db, Company

company_routes = Blueprint('companies', __name__)

# Get all companies
@company_routes.route('/', methods=['GET'])
@login_required
def get_companies():
    companies = Company.query.all()
    return {'companies': [company.to_dict() for company in companies]}

# Get a single company
@company_routes.route('/<int:id>', methods=['GET'])
@login_required
def get_company(id):
    company = Company.query.get(id)
    if not company:
        return {"errors": ["Company not found"]}, 404
    return company.to_dict()

# Create a new company
@company_routes.route('/', methods=['POST'])
@login_required
def create_company():
    data = request.get_json()
    name = data.get('name')
    tax_id = data.get('tax_id')

    if not name or not tax_id:
        return {"errors": ["Name and Tax ID are required"]}, 400

    company = Company(
        name=name,
        tax_id=tax_id,
        street=data.get('street'),
        city=data.get('city'),
        county=data.get('county'),
        state=data.get('state'),
        zipcode=data.get('zipcode'),
        phone=data.get('phone'),
        email=data.get('email')
    )
    db.session.add(company)
    db.session.commit()
    return company.to_dict(), 201

# Update company
@company_routes.route('/<int:id>', methods=['PUT'])
@login_required
def update_company(id):
    company = Company.query.get(id)
    if not company:
        return {"errors": ["Company not found"]}, 404

    data = request.get_json()
    company.name = data.get('name', company.name)
    company.tax_id = data.get('tax_id', company.tax_id)
    company.street = data.get('street', company.street)
    company.city = data.get('city', company.city)
    company.county = data.get('county', company.county)
    company.state = data.get('state', company.state)
    company.zipcode = data.get('zipcode', company.zipcode)
    company.phone = data.get('phone', company.phone)
    company.email = data.get('email', company.email)

    db.session.commit()
    return company.to_dict()

# Delete company
@company_routes.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_company(id):
    company = Company.query.get(id)
    if not company:
        return {"errors": ["Company not found"]}, 404

    db.session.delete(company)
    db.session.commit()
    return {"message": "Successfully deleted"}
