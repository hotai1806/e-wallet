""" AuthenticationDecorator"""
from functools import wraps

from flask import abort, request, make_response

from src.helper.jwt_helper import decode_auth_token
from src.models.merchant import Merchant
from src.models.account import Account


def authentication_required(*list_account_type):
    def authentication_decorator(function_api):
        """
        Return user_id with type number

        """

        @wraps(function_api)
        def decorated_function(*args, **kws):
            if not 'Authorization' in request.headers:
                abort(401)

            user = None

            data = request.headers['Authorization']
            token = str.replace(str(data), 'Bearer ', '')
            try:
                user_id_not_verify = decode_auth_token(token)['user']
                user_check_type = Account.query.filter_by(
                    account_id=user_id_not_verify).first()
                if user_check_type.account_type not in list_account_type:
                    abort(403)
                api_key = Merchant.query.filter_by(
                    account_id=user_check_type.account_id).first().api_key
                if not api_key:
                    abort(401)
                payload_jwt = decode_auth_token(token, api_key)

            except Exception as error:
                message_error = error.to_dict()
                response = make_response(
                    {"message": message_error["message"]}, message_error["status_code"])
                return response

            return function_api(payload_jwt, *args, **kws)

        return decorated_function
    return authentication_decorator
