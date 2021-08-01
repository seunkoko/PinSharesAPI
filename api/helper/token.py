import os
import datetime

from flask_jwt import jwt

def generate_authorization_token(id):
    """ Generate authorization token """
    token_date = datetime.datetime.utcnow()

    payload = {
        "id": id,
        "stamp": str(token_date),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    return jwt.encode(payload, os.getenv("TOKEN_KEY"), algorithm='HS256').decode('utf-8')
