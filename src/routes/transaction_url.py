""" Transaction Blueprint"""
from flask import Blueprint
from src.controllers.transaction_controller import create_transaction
transaction_bp = Blueprint('transaction_bp', __name__)

# Route: /transactions/{action}
transaction_bp.route('/', methods=['POST'])(create_transaction)
# account_bp.route('/', methods=['POST'])(create_account)
# account_bp.route('/<accountId>/topup', methods=['POST'])(get_account_token)

# cart_bp.route('/update_quantity/<product_id>', methods=['PUT'])(update_quantity)
