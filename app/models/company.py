from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime

class Company(db.Model):
    __tablename__ = 'companies'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    tax_id = db.Column(db.String(100), unique=True, nullable=False)
    street = db.Column(db.String(255))
    city = db.Column(db.String(100))
    county = db.Column(db.String(100))
    state = db.Column(db.String(50))
    zipcode = db.Column(db.String(20))
    phone = db.Column(db.String(50))
    email = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    # Relationships
    users = db.relationship('UserCompany', back_populates='company', cascade="all, delete-orphan")
    approvers = db.relationship('Approver', back_populates='company', cascade="all, delete-orphan")
    vendors = db.relationship('Vendor', back_populates='company', cascade="all, delete-orphan")
    categories = db.relationship('Category', back_populates='company', cascade="all, delete-orphan")
    invoices = db.relationship('Invoice', back_populates='company', cascade="all, delete-orphan")
    payments = db.relationship('Payment', back_populates='company', cascade="all, delete-orphan")
    payment_batches = db.relationship('PaymentBatch', back_populates='company', cascade="all, delete-orphan")
    bank_balances = db.relationship('BankBalance', back_populates='company', cascade="all, delete-orphan")
    audit_logs = db.relationship('AuditLog', back_populates='company', cascade="all, delete-orphan")
    users = db.relationship('UserCompany', back_populates='company', cascade="all, delete-orphan") # Relationship with UserCompany
    approvers = db.relationship('Approver', back_populates='company', cascade="all, delete-orphan") # Relationship with Approver
    vendors = db.relationship('Vendor', back_populates='company', cascade="all, delete-orphan")
    categories = db.relationship('Category', back_populates='company', cascade="all, delete-orphan")
    invoices = db.relationship('Invoice', back_populates='company', cascade="all, delete-orphan")




    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'tax_id': self.tax_id,
            'street': self.street,
            'city': self.city,
            'county': self.county,
            'state': self.state,
            'zipcode': self.zipcode,
            'phone': self.phone,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
