from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime

class Invoice(db.Model):
    __tablename__ = 'invoices'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(
        db.Integer,
        db.ForeignKey(add_prefix_for_prod("companies.id")),
        nullable=False
    )
    vendor_id = db.Column(
        db.Integer,
        db.ForeignKey(add_prefix_for_prod("vendors.id")),
        nullable=False
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey(add_prefix_for_prod("users.id")),
        nullable=False
    )
    category_id = db.Column(
        db.Integer,
        db.ForeignKey(add_prefix_for_prod("categories.id")),
        nullable=False
    )
    invoice_number = db.Column(db.String(100), nullable=False)
    invoice_date = db.Column(db.Date, nullable=False)
    voucher_date = db.Column(db.Date)
    due_date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(50), default='pending')  # pending, approved, paid
    approved_by = db.Column(
        db.Integer,
        db.ForeignKey(add_prefix_for_prod("users.id")),
        nullable=True
    )
    approval_date = db.Column(db.Date)
    description = db.Column(db.Text)
    attachment_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    company = db.relationship('Company', back_populates='invoices')
    vendor = db.relationship('Vendor', back_populates='invoices')
    category = db.relationship('Category', back_populates='invoices')
    user = db.relationship('User', back_populates='invoices_created', foreign_keys=[user_id])
    approver = db.relationship('User', back_populates='invoices_approved', foreign_keys=[approved_by])
    payments = db.relationship('Payment', back_populates='invoice', cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'company_id': self.company_id,
            'vendor_id': self.vendor_id,
            'user_id': self.user_id,
            'category_id': self.category_id,
            'invoice_number': self.invoice_number,
            'invoice_date': self.invoice_date.isoformat(),
            'voucher_date': self.voucher_date.isoformat() if self.voucher_date else None,
            'due_date': self.due_date.isoformat(),
            'amount': float(self.amount),
            'status': self.status,
            'approved_by': self.approved_by,
            'approval_date': self.approval_date.isoformat() if self.approval_date else None,
            'description': self.description,
            'attachment_url': self.attachment_url,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
