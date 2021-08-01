from api import models
from functools import wraps
from flask import request, jsonify, g

from ..models import Users
from ..helper import pin_errors

def validate_request():
    """ This method validates the Request payload.
    Args
        expected_args(tuple): where i = 0 is type and i > 0 is argument to be
                            validated
    Returns
      f(*args, **kwargs)
    """

    def real_validate_request(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not request.json:
                return pin_errors(
                    'Request must be a valid JSON',
                    400
                )
            return f(*args, **kwargs)

        return decorated

    return real_validate_request


def validate_user():
    """ This method validates the user, if they exist and if they are active.
    Args
        expected_args(tuple): where i = 0 is type and i > 0 is argument to be
                            validated
    Returns
      f(*args, **kwargs)
    """

    def real_validate_user(f):
        @wraps(f)
        def decorated(*args,**kwargs):
            user_id = g.current_user_id
           
            # validate user already exists
            _user = Users.get_by_id(user_id)

            if not _user:
                return pin_errors('User does not exist', 400)

            if not _user.is_active:
                return pin_errors('This account is not active, please activate.', 400)

            g.user = _user

            return f(*args, **kwargs)

        return decorated

    return real_validate_user
