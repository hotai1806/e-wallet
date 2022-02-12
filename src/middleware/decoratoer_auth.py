""" AuthenticationDecorator"""
from functools import wraps

from flask import abort, request, make_response

from src.helper.jwt_helper import decode_auth_token


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
            user = decode_auth_token(token)
        except Exception as error:
            message_error = error.to_dict()
            response = make_response({"message": message_error["message"]}, message_error["status_code"])
            return response

        return function_api(user, *args, **kws)

    return decorated_function
