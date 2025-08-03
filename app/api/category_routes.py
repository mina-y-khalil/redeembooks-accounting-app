from flask import Blueprint, request
from flask_login import login_required, current_user
from app.models import db, Category

category_routes = Blueprint('categories', __name__)

# Get All Categories
@category_routes.route('/companies/<int:company_id>/categories', methods=['GET'])
@login_required
def get_categories(company_id):
    categories = Category.query.filter_by(company_id=company_id).all()
    return {"categories": [category.to_dict() for category in categories]}, 200

# Get Category by ID
@category_routes.route('/categories/<int:id>', methods=['GET'])
@login_required
def get_category(id):
    category = Category.query.get(id)
    if not category:
        return {"errors": ["Category not found"]}, 404
    return category.to_dict(), 200

# Create Category
@category_routes.route('/companies/<int:company_id>/categories', methods=['POST'])
@login_required
def create_category(company_id):
    data = request.get_json()
    category = Category(
        company_id=company_id,
        name=data.get('name'),
        description=data.get('description')
    )
    db.session.add(category)
    db.session.commit()
    return category.to_dict(), 201

# Update Category
@category_routes.route('/categories/<int:id>', methods=['PUT'])
@login_required
def update_category(id):
    category = Category.query.get(id)
    if not category:
        return {"errors": ["Category not found"]}, 404
    
    data = request.get_json()
    if 'name' in data:
        category.name = data['name']
    if 'description' in data:
        category.description = data['description']

    db.session.commit()
    return category.to_dict(), 200

# ✅ Delete Category
@category_routes.route('/categories/<int:id>', methods=['DELETE'])
@login_required
def delete_category(id):
    category = Category.query.get(id)
    if not category:
        return {"errors": ["Category not found"]}, 404
    
    db.session.delete(category)
    db.session.commit()
    return {"message": "Successfully deleted"}, 200
