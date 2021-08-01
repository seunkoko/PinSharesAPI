from functools import wraps

from flask import request, jsonify, g
from flask_jwt import jwt


def authorize_app_access(f):
    """ This method authorizes user with authorization token.
    Args
        expected_args(tuple): where i = 0 is type and i > 0 is argument to be
                            validated
    Returns
      f(*args, **kwargs)
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        user_token = request.headers.get('authorization')

        if not user_token:
            response = jsonify({
                "status": "fail",
                "data": {
                    "message": "Bad request. Header does not contain"
                               " Authorization token"
                }
            })
            response.status_code = 401
            return response

        unauthorized_response = jsonify({
            "status": "fail",
            "data": {
                "message": "Unauthorized. The authorization token supplied"
                        " is invalid"
            }
        })
        unauthorized_response.status_code = 401
        expired_response = jsonify({
            "status": "fail",
            "data": {
                "message": "The authorization token supplied is expired"
            }
        })
        expired_response.status_code = 401

        try:
            # decode token
            payload = jwt.decode(user_token, 'secret',
                                 options={"verify_signature": False})
        except jwt.ExpiredSignatureError:
            return expired_response
        except jwt.InvalidTokenError:
            return unauthorized_response

        # confirm that payload has required keys
        if ("id") not in payload.keys():
            return unauthorized_response
        else:
            # set current user in flask global variable, g
            g.current_user_id = payload["id"]
            g.token_info = payload

        return f(*args, **kwargs)

    return decorated
