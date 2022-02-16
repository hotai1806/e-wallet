""" Login controllers"""
from flask import request, make_response

from src.helper.jwt_helper import encode_auth_token
from src.models.account import Account
from src.models.models_base import db
from src.constants.account_type_constants import AccountType
from src.constants.message_constant import ErrorMessage, SuccessMessage


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
    return make_response({'accountType': account.account_type,
                         'accountId': account.account_id, 'balance': account.balance}, 200)


def top_up(accountId):
    """api top up account

    Returns:
        [message]: [string]
    """
    account_id = request.get_json()['accountId']
    amount = request.get_json()['amount']

    if not account_id or not amount:
        return make_response(ErrorMessage.INVALID_DATA_INPUT)

    account = Account.query.filter_by(account_id=account_id).first()
    if not account:
        return make_response(ErrorMessage.INVALID_ACCOUNT)

    account.balance += amount
    db.session.commit()
    return make_response({'accountType': account.account_type, 'accountId': account.account_id, 'balance': account.balance}, 200)
    # return make_response(SuccessMessage.CREATE_SUCCESS)
