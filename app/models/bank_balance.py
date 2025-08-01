from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime

class BankBalance(db.Model):
    __tablename__ = 'bank_balances'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(
        db.Integer,
        db.ForeignKey(add_prefix_for_prod("companies.id")),
        nullable=False
    )
    balance = db.Column(db.Numeric(12, 2), nullable=False)
    effective_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    company = db.relationship('Company', back_populates='bank_balances')

    def to_dict(self):
        return {
            'id': self.id,
            'company_id': self.company_id,
            'balance': float(self.balance),
            'effective_date': self.effective_date.isoformat(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
