from api.schema import user_schema
import os
import datetime

from flask import g, request, jsonify, url_for
from marshmallow import ValidationError
from flask_restful import Resource

from ..models import (
    Users
)
from ..schema import (
    UserSchema
)
from ..auth import (
    authorize_app_access,
    validate_request, validate_user
)
from ..helper import (
    pin_success, pin_errors, generate_authorization_token
)


class UserSignUpResource(Resource):
    """ User SignUp Resource
        POST /signup
    """

    @validate_request()
    def post(self):
        """ Signs up users """
        # get data from request body
        _data = request.get_json()

        # create user schema and validate data
        user_schema = UserSchema()
        _validated_data = None

        try:
            _validated_data = user_schema.load(_data)
        except ValidationError as err:
            return pin_errors(err.messages, 400)

        # check if user already exists
        _user_exists = Users.find_first(**{
            'username': _validated_data['username'].lower()
        })
        if _user_exists:
            return pin_errors('Username already exists', 400)

        # create new user
        new_user = Users(
            username=_validated_data['username'].lower()
        )
        new_user.set_password(_validated_data['password'])

        try:
            _user = new_user.save()
        except:
            return pin_errors('Something went wrong', 500)

        # generate authorization token
        _token = generate_authorization_token(_user.id)

        # return success message
        return pin_success(
            message='User signed up successfully',
            response_data={
                "token": str(_token)
            },
            status_code=201
        )


class UserLoginResource(Resource):
    """ User Login Resource
        POST /login
    """

    @validate_request()
    def post(self):
        """ Logs in users """
        # get data from request body
        _data = request.get_json()

        # create user schema and validate data
        user_schema = UserSchema()
        _validated_data = None

        try:
            _validated_data = user_schema.load(_data)
        except ValidationError as err:
            return pin_errors(err.messages, 400)

        # get user
        _user = Users.find_first(**{
            'username': _validated_data['username'].lower()
        })

        # handle user not found
        if not _user:
            return pin_errors('Invalid username or password', 400)
        
        # confirm user password
        if not _user.check_password(_validated_data['password']):
            return pin_errors('Invalid username or password', 400)

        # generate authorization token
        _token = generate_authorization_token(_user.id)

        # return success message
        return pin_success(
            message='User login successful',
            response_data={
                "token": str(_token)
            },
            status_code=200
        )
        
