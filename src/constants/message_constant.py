class ErrorMessage(object):
    INVALID_USER_TYPE = {"message": "Invalid user type"}, 400
    INVALID_DATA_INPUT = {"message": "Invalid data input"}, 400
    INVALID_MERCHANT_ID = {"message": "Invalid merchant id"}, 400
    INVALID_SIGNATURE = {"message": "Invalid signature"}, 400


class ErrorTransactionMessage(object):
    TRANSACTION_NOT_INITIALIZED = {
        "message": "Transaction not initialized"},   400
    TRANSACTION_NOT_CONFIRMED = {
        "message": "Transaction not confirmed"},   400
    TRANSACTION_FAILED = {"message": "Transaction failed"}, 400
    TRANSACTION_COMPLETED = {"message": "Transaction already completed"}, 400


class UserMessage:
    BALANCE_NOT_ENOUGH = {"message": "Balance not enough"}, 400


class SuccessMessage:
    CREATE_SUCCESS = {"message": "Success"}, 200
    CONFIRM_SUCCESS = {"message": "Success", "code": "SUC"}, 200
    VERIFY_SUCCESS = {"message": "Success", "code": "SUC"}, 200
    CANCEL_SUCCESS = {"message": "Success", "code": "SUC"}, 200
