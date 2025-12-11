import jwt
from flask import request
from functools import wraps

jwt_secret_key="this is secret key to generate jwt token"

def authentication(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        token=request.headers.get("token")
        if not token:
            return {"message":'Forbidden access'}

        try:
            jwt.decode(token, jwt_secret_key, algorithms='HS256')
        except jwt.ExpiredSignatureError:
            return {"message":'Forbidden access'}, 401
        except jwt.InvalidTokenError:
            return {"message":'Invalid Token'}, 401

        return func(*args, **kwargs)
    return wrapper