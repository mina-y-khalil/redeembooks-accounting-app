from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime

class Vendor(db.Model):
    __tablename__ = 'vendors'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(
        db.Integer,
        db.ForeignKey(add_prefix_for_prod("companies.id")),
        nullable=False
    )
    name = db.Column(db.String(255), nullable=False)
    contact_name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    phone = db.Column(db.String(50))
    tax_id = db.Column(db.String(100))
    street = db.Column(db.String(255))
    city = db.Column(db.String(100))
    county = db.Column(db.String(100))
    state = db.Column(db.String(50))
    zipcode = db.Column(db.String(20))
    preferred_payment_method = db.Column(db.String(50))
    payment_terms = db.Column(db.String(50))
    w9_document_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    company = db.relationship('Company', back_populates='vendors')
    invoices = db.relationship('Invoice', back_populates='vendor', cascade="all, delete-orphan")
    payments = db.relationship('Payment', back_populates='vendor', cascade="all, delete-orphan")
    invoices = db.relationship('Invoice', back_populates='vendor', cascade="all, delete-orphan")
    payments = db.relationship('Payment', back_populates='vendor', cascade="all, delete-orphan")



    def to_dict(self):
        return {
            'id': self.id,
            'company_id': self.company_id,
            'name': self.name,
            'contact_name': self.contact_name,
            'email': self.email,
            'phone': self.phone,
            'tax_id': self.tax_id,
            'street': self.street,
            'city': self.city,
            'county': self.county,
            'state': self.state,
            'zipcode': self.zipcode,
            'preferred_payment_method': self.preferred_payment_method,
            'payment_terms': self.payment_terms,
            'w9_document_url': self.w9_document_url,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
