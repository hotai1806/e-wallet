from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID

from src.models.account import Account
from src.models.models_base import db


class Merchant(db.Model):
    __tablename__ = "merchants"

    merchant_id = db.Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False
    )
    account_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("accounts.account_id"),
        default=uuid4,
        nullable=False,
    )
    merchant_name = db.Column(db.String(200), nullable=False)
    merchant_url = db.Column(db.String(200), nullable=False)
    api_key = db.Column(UUID(as_uuid=True), default=uuid4, nullable=False)
    # join table
    account = db.relationship(Account, backref="merchants")

    def __init__(self, account_id, merchant_name, merchant_url):
        self.account_id = account_id
        self.merchant_name = merchant_name
        self.merchant_url = merchant_url
