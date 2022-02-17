""" Merchant controllers"""
# third party api
from flask import request, make_response

# local source
from src.constants.account_type_constants import AccountType
from src.models.merchant import Merchant
from src.models.account import Account
from src.models.models_base import db
from src.constants.message_constant import ErrorMessage

mock_data = {
    "merchantName": "string",
    "accountId": "e5cc7ef9-8da1-4ca9-9df5-46cc08c98760",
    "merchantId": "dd6de58e-fc7b-4138-bb4a-bd70be05689a",
    "apiKey": "bdd6a784-0da5-45da-a83c-7bbe1d34db35",
    "merchantUrl": "http://localhost:8080",
}


def sign_up_merchant():
    """
    controller submit login api POST
    return access_token: string || None
    """
    body_data = request.get_json()
    merchant_name = body_data["merchantName"]
    merchant_url = body_data["merchantUrl"]
    if not merchant_name or not merchant_url:
        return make_response(ErrorMessage.INVALID_DATA_INPUT)
    account_merchant = Account(account_type=AccountType.MERCHANT.value)
    db.session.add(account_merchant)

    db.session.flush()
    db.session.refresh(account_merchant)

    merchant = Merchant(
        merchant_name=merchant_name,
        merchant_url=merchant_url,
        account_id=account_merchant.account_id,
    )
    db.session.add(merchant)
    db.session.commit()
    data_response = {
        "merchantName": merchant.merchant_name,
        "merchantId": merchant.merchant_id,
        "apiKey": merchant.api_key,
        "merchantUrl": merchant.merchant_url,
        "accountId": merchant.account_id,
    }

    response = make_response(data_response)
    return response
