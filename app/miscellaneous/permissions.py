from functools import wraps

from flask import jsonify
from flask_jwt_extended import (
    verify_jwt_in_request, get_jwt
)
from app.database.roles import UserType


def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["role"] == UserType.ADMIN.value:
                return fn(*args, **kwargs)
            else:
                response = jsonify(msg='Admins only!')
                response.status_code = 403
                return response
        return decorator
    return wrapper
