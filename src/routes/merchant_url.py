""" Merchant Blueprint"""
from flask import Blueprint
from src.controllers.merchant_controller import sign_up_merchant

merchant_bp = Blueprint("marchant", __name__)

# Route: /merchant/{action}
merchant_bp.route("/", methods=["POST"])(sign_up_merchant)
