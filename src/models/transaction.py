from src.models.models_base import db
from src.models.account import Account
from src.models.merchant import Merchant
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4


class Transaction(db.Model):
    __tablename__ = "transactions"

    transaction_id = db.Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False
    )
    merchant_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("merchants.merchant_id"),
        default=uuid4,
        nullable=False,
    )
    incomeAccount = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("accounts.account_id"),
        default=uuid4,
        nullable=False,
    )
    outcomeAccount = db.Column(
        UUID(as_uuid=True), db.ForeignKey("accounts.account_id"), nullable=True
    )
    amount = db.Column(db.Float, nullable=False)
    extraData = db.Column(db.String(255))
    signature = db.Column(db.String(255))
    status = db.Column(
        db.Enum(
            "INITIALIZED",
            "CONFIRMED",
            "VERIFYED",
            "CANCELED",
            "EXPIRED",
            "FAILED",
            "COMPLETED",
            name="transactions_status",
            create_type=False,
        ),
        nullable=False,
    )

    # join table
    merchant = db.relationship(Merchant, backref="transactions")
    income_account = db.relationship(Account, foreign_keys=[incomeAccount])
    outcome_account = db.relationship(Account, foreign_keys=[outcomeAccount])

    def __init__(
        self,
        merchantId,
        incomeAccount,
        outcomeAccount,
        amount,
        status,
        extraData,
        signature,
    ):
        self.merchant_id = merchantId
        self.incomeAccount = incomeAccount
        self.outcomeAccount = outcomeAccount
        self.amount = amount
        self.extraData = extraData
        self.signature = signature
        self.status = status
