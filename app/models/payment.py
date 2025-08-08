from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime

class Payment(db.Model):
    __tablename__ = 'payments'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(
        db.Integer,
        db.ForeignKey(add_prefix_for_prod("companies.id")),
        nullable=False
    )
    invoice_id = db.Column(
        db.Integer,
        db.ForeignKey(add_prefix_for_prod("invoices.id")),
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
    payment_date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    method = db.Column(db.String(50), nullable=False)  # ACH, Check, Wire
    reference_number = db.Column(db.String(100))
    notes = db.Column(db.Text)
    batch_id = db.Column(
        db.Integer,
        db.ForeignKey(add_prefix_for_prod("payment_batches.id")),
        nullable=True
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    company = db.relationship('Company', back_populates='payments')
    invoice = db.relationship('Invoice', back_populates='payments')
    vendor = db.relationship('Vendor', back_populates='payments')
    user = db.relationship('User', back_populates='payments')
    batch = db.relationship('PaymentBatch', back_populates='payments')

    def to_dict(self):
        return {
            'id': self.id,
            'company_id': self.company_id,
            'invoice_id': self.invoice_id,
            'vendor_id': self.vendor_id,
            'user_id': self.user_id,
            'payment_date': self.payment_date.isoformat(),
            'amount': float(self.amount),
            'method': self.method,
            'reference_number': self.reference_number,
            'notes': self.notes,
            'batch_id': self.batch_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
