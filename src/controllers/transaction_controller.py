""" Transaction controllers"""
# third party api
from flask import request, make_response
import hashlib
import json
import requests
from src.constants.account_type_constants import AccountType
from src.models.account import Account

# local source
from src.models.transaction import Transaction
from src.models.models_base import db
from src.constants.message_constant import (ErrorMessage,
                                            SuccessMessage, UserMessage,
                                            ErrorTransactionMessage)
from src.constants.status_transaction_constants import StatusTransaction
from src.middleware.decoratoer_auth import authentication_required
from src.helper.log_helper import setup_logging
logger = setup_logging()

url_update = "http://127.0.0.1:8000/order/"


def change_status_transaction(status, transaction_id):
    import psycopg2
    conn = psycopg2.connect(host="localhost", port=5433,
                            database="shopping", user="admin",
                            password="youknow")
    # Log in to the database
    logger.info(status)
    logger.info(transaction_id)
    # Create a cursor object
    cur = conn.cursor()
    query = "SELECT * from transactions  WHERE transaction_id = %s"

    cur.execute(query, [transaction_id])
    transaction = cur.fetchall()
    if transaction[-1][-1] == StatusTransaction.COMPLETED:
        return None
    query = "UPDATE transactions SET status = %s WHERE transaction_id = %s"
    cur.execute(query, (status, transaction_id))
    cur.close()
    conn.commit()
    return None


@authentication_required(AccountType.MERCHANT.value)
def create_transaction(payload_jwt):
    """
    controller submit login api POST
    return access_token: string || None
    """
    from threading import Timer
    # Extract data from body
    body_data = request.form.to_dict()
    merchant_id = body_data["merchantId"]
    extraData = int(body_data["extraData"])
    amount = float(body_data["amount"])
    signature_body = body_data["signature"]

    # Prepare data to check signature
    data_check_signature = {
        "merchantId": merchant_id,
        "amount": amount,
        "extraData": extraData,
    }
    signature = hashlib.md5(
        json.dumps(data_check_signature, sort_keys=True).encode("utf-8")
    ).hexdigest()
    if signature != payload_jwt["signature"] != signature_body:
        return make_response(ErrorMessage.INVALID_SIGNATURE)

    if not merchant_id or not extraData or not amount:
        return make_response(ErrorMessage.INVALID_DATA_INPUT)

    transaction = Transaction(
        merchantId=merchant_id,
        amount=amount,
        status=StatusTransaction.INITIALIZED.value,
        incomeAccount=payload_jwt["user"],
        outcomeAccount=None,
        extraData=extraData,
        signature=signature,
    )
    db.session.add(transaction)
    db.session.commit()

    data_response = {
        "transactionId": transaction.transaction_id,
        "merchantId": transaction.merchant_id,
        "incomeAccount": transaction.incomeAccount,
        "outcomeAccount": transaction.outcomeAccount,
        "amount": transaction.amount,
        "signature": signature,
        "extraData": transaction.extraData,
        "status": transaction.status,
    }
    Timer(300, change_status_transaction, [
          StatusTransaction.CANCELED.value,
          transaction.transaction_id]).start()

    return make_response(data_response, 200)


@authentication_required(AccountType.PERSONAL.value)
def confirm_transaction(payload_jwt):
    """Api confirm transaction
    return "code: "SUC" , "message"
    """
    body_data = request.form.to_dict()
    transactionId = body_data["transactionId"]
    transaction = Transaction.query.filter_by(
        transaction_id=transactionId).first()

    if transaction.status != StatusTransaction.INITIALIZED.value:
        requests.put(url_update + str(transaction.extraData),
                     data={"status": StatusTransaction.FAILED.value})
        return make_response(
            ErrorTransactionMessage.TRANSACTION_NOT_INITIALIZED)
    account = Account.query.filter_by(account_id=payload_jwt["user"]).first()
    if account.balance < transaction.amount:
        transaction.status = StatusTransaction.FAILED.value
        db.session.commit()
        requests.put(url_update + str(transaction.extraData),
                     data={"status": StatusTransaction.FAILED.value})
        return make_response(UserMessage.BALANCE_NOT_ENOUGH)

    transaction.status = StatusTransaction.CONFIRMED.value
    transaction.outcomeAccount = payload_jwt["user"]
    db.session.commit()
    return make_response(SuccessMessage.CONFIRM_SUCCESS)


@authentication_required(AccountType.PERSONAL.value)
def verify_transaction(payload_jwt):
    """Api verify transaction
    return "code: "SUC" , "message"
    """
    body_data = request.form.to_dict()
    transactionId = body_data["transactionId"]
    transaction = Transaction.query.filter_by(
        transaction_id=transactionId).first()
    if transaction.status != StatusTransaction.VERIFYED.value:
        return make_response(SuccessMessage.VERIFY_SUCCESS)
    if transaction.status != StatusTransaction.CONFIRMED.value:
        return make_response(ErrorTransactionMessage.TRANSACTION_NOT_CONFIRMED)
    if transaction.status == StatusTransaction.FAILED.value:
        return make_response(ErrorTransactionMessage.TRANSACTION_FAILED)
    if transaction.outcome_account.balance < transaction.amount:
        transaction.status = StatusTransaction.FAILED.value
        db.session.commit()
        return make_response(UserMessage.BALANCE_NOT_ENOUGH)
    transaction.outcome_account.balance -= transaction.amount
    transaction.income_account.balance += transaction.amount
    transaction.status = StatusTransaction.VERIFYED.value
    db.session.commit()

    requests.put(url_update + str(transaction.extraData),
                 data={
        "status": StatusTransaction.COMPLETED.value
    })
    return make_response(SuccessMessage.TRANSACTION_COMPLETED)


@authentication_required(AccountType.PERSONAL.value)
def cancel_transaction(payload_jwt):
    """Api cancel transaction
    return "code: "SUC" , "message"
    """
    body_data = request.form.to_dict()
    transactionId = body_data["transactionId"]
    transaction = Transaction.query.filter_by(
        transaction_id=transactionId).first()
    # check status cancel equal to cancel
    if transaction.status == StatusTransaction.CANCELED.value:
        return make_response(SuccessMessage.CANCEL_SUCCESS)
    if transaction.status == StatusTransaction.COMPLETED.value:
        return make_response(ErrorTransactionMessage.TRANSACTION_COMPLETED)
    transaction.status = StatusTransaction.CANCELED.value
    db.session.commit()
    return make_response(SuccessMessage.CANCEL_SUCCESS)
