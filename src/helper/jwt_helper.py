""" jwt verifying module"""
import datetime

import jwt

from src.setting import SECRET_KEY


class InvalidAPIUsage(Exception):
    status_code = 400
    message = "Invalid API Usage"

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
    def __str__(self):
        return self.message

    def to_dict(self):

        return {"message": self.message, "status_code": self.status_code}


def encode_auth_token(user_id):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=200),
            'iat': datetime.datetime.utcnow(),
            'user': user_id
        }
        return jwt.encode(
            payload,
            SECRET_KEY,
            algorithm='HS256'
        )
    except Exception as error:
        raise error


def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, SECRET_KEY, algorithms=['HS256'])
        return payload['user']
    except jwt.ExpiredSignatureError:
        raise InvalidAPIUsage('Signature expired. Please log in again.', 401)
    except jwt.InvalidTokenError:
        raise InvalidAPIUsage('Invalid token. Please log in again.', 401)
