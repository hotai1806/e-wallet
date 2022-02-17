""" Transaction Blueprint"""
from flask import Blueprint
from src.controllers.transaction_controller import (
    create_transaction,
    confirm_transaction,
    cancel_transaction,
    verify_transaction,
)

transaction_bp = Blueprint("transaction_bp", __name__)

# Route: /transactions/{action}
transaction_bp.route("/", methods=["POST"])(create_transaction)
transaction_bp.route("/confirm", methods=["POST"])(confirm_transaction)
transaction_bp.route("/verify", methods=["POST"])(verify_transaction)
transaction_bp.route("/`cancel`", methods=["POST"])(cancel_transaction)
