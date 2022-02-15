""" Transaction controllers"""
# third party api
from flask import request, make_response, jsonify
import hashlib
import json
from src.constants.account_type_constants import AccountType

# local source
from src.models.transaction import Transaction
from src.models.merchant import Merchant
from src.models.models_base import db

from src.constants.message_constant import ErrorMessage, SuccessMessage
from src.constants.status_transaction_constants import StatusTransaction
from src.middleware.decoratoer_auth import authentication_required

mock_request_create_transaction = {
    "merchantId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "amount": 0,
    "extraData": "string",
    "signature": "string"
}

mock_response_create_transaction = {
    "transactionId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "merchantId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "incomeAccount": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "outcomeAccount": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "amount": 0,
    "extraData": "string",
    "signature": "225744eba143248ae232bf81d6366b66",
    "status": "INITIALIZED"
}


@authentication_required(AccountType.MERCHANT.value)
def create_transaction(payload_jwt):
    """
    controller submit login api POST
    return access_token: string || None
    """
    body_data = request.form.to_dict()
    print(body_data)
    merchant_id = body_data['merchantId']
    extraData = body_data['extraData']
    amount = int(body_data['amount'])

    data_check_signature = {
        "merchantId": merchant_id,
        "amount": amount,
        "extraData": extraData
    }

    signature = hashlib.md5(json.dumps(
        data_check_signature, sort_keys=True).encode('utf-8')).hexdigest()

    print(signature)
    print(payload_jwt['signature'])
    if signature != payload_jwt['signature']:
        return make_response(ErrorMessage.INVALID_SIGNATURE)

    if not merchant_id or not extraData or not amount:
        return make_response(ErrorMessage.INVALID_DATA_INPUT)

    transaction = Transaction(
        merchantId=merchant_id, amount=amount,
        status=StatusTransaction.CREATE.value,
        incomeAccount=payload_jwt['user'],
        outcomeAccount=None,
        extraData=extraData, signature=signature)
    print(payload_jwt['user'])
    print(transaction.income_account)
    db.session.add(transaction)
    db.session.commit()
    data_response = {
        "transactionId": transaction.transaction_id,
        "merchantId": transaction.merchant_id,
        "incomeAccount": transaction.incomeAccount,
        "outcomeAccount": transaction.outcomeAccount,
        "amount": transaction.amount, 'signature': signature,
        'extraData': transaction.extraData, 'status': transaction.status}
    response = make_response(data_response,200)
    return response
