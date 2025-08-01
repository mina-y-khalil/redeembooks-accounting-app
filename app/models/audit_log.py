from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey(add_prefix_for_prod("users.id")),
        nullable=False
    )
    company_id = db.Column(
        db.Integer,
        db.ForeignKey(add_prefix_for_prod("companies.id")),
        nullable=False
    )
    action = db.Column(db.String(255), nullable=False)  # CREATE, UPDATE, DELETE, APPROVE, PAY
    table_name = db.Column(db.String(255), nullable=False)
    record_id = db.Column(db.Integer, nullable=False)
    old_data = db.Column(db.Text)
    new_data = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='audit_logs')
    company = db.relationship('Company', back_populates='audit_logs')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'company_id': self.company_id,
            'action': self.action,
            'table_name': self.table_name,
            'record_id': self.record_id,
            'old_data': self.old_data,
            'new_data': self.new_data,
            'created_at': self.created_at.isoformat()
        }
