from .models_base import db
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4


class Account(db.Model):
    __tablename__ = "accounts"

    account_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False)
    account_type = db.Column(db.Enum("merchant", "personal", "issuer", name="acc_type", create_type=False),
                             nullable=False)
    balance = db.Column(db.Float, default=0)

    def __init__(self, account_type):
        self.account_type = account_type
        self.balance = 0

    def __repr__(self):
        return f'<User {self.account_id!r}>'

    @property
    def serialize(self):
        """Return object data in easily serializable format likely JSON"""
        return {
            'account_id': self.account_id,
            'account_type': self.account_type,
            'balance': self.balance,

        }

    def top_up(self, amount):
        self.balance += amount
