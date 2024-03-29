""" Account Blueprint"""
from flask import Blueprint
from src.controllers.account_controller import (
    get_account_token, create_account, top_up
)
account_bp = Blueprint("account_bp", __name__)

# Route: /accounts/{action}
account_bp.route("/<accountId>/token", methods=["GET"])(get_account_token)
account_bp.route("/", methods=["POST"])(create_account)
account_bp.route("/<accountId>/topup", methods=["POST"])(top_up)
