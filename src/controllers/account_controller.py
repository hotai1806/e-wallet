""" Login controllers"""
from flask import request, make_response

from src.helper.jwt_helper import encode_auth_token
from src.models.account import Account
from src.models.models_base import db
from src.constants.account_type_constants import AccountType
from src.constants.message_constant import ErrorMessage , SuccessMessage


def get_account_token(accountId):
    """
    controller submit login api POST
    return access_token: string || None
    """
    if not accountId:
        return make_response({"message": "Invalid account"}, 401)

    access_token = encode_auth_token(accountId)
    response = make_response({"access_token": access_token}, 200)
    return response


def create_account():
    """api create account base account_type

    Returns:
        [message]: [string]
    """
    account_type = request.get_json()['accountType']

    if account_type not in AccountType._value2member_map_:
        return make_response(ErrorMessage.INVALID_USER_TYPE)

    account = Account(account_type=account_type)
    db.session.add(account)
    db.session.commit()
    return make_response(SuccessMessage.CREATE_SUCCESS)

