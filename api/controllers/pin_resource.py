from api.schema.pin_schema import PinSchema, PinUserInfoSchema
from api.schema import user_schema
import os
import datetime

from flask import g, request, jsonify, url_for
from marshmallow import ValidationError
from flask_restful import Resource

from ..models import (
    Pins, PinShares
)
from ..schema import (
    PinSchema, PinInfoSchema
)
from ..auth import (
    authorize_app_access,
    validate_request, validate_user
)
from ..helper import (
    pin_success, pin_errors, generate_authorization_token
)


class PinListResource(Resource):
    """ PinList Resource
        POST /pin
    """

    @authorize_app_access
    @validate_user()
    @validate_request()
    def post(self):
        """ Add new Pin """
        # get data from request body
        _data = request.get_json()
        _data['user_id'] = g.current_user_id

        # create pin schema and validate data
        pin_schema = PinSchema()
        _validated_data = None

        try:
            _validated_data = pin_schema.load(_data)
        except ValidationError as err:
            return pin_errors(err.messages, 400)

        # add new pin
        new_pin = Pins(
            user_id=_validated_data['user_id'],
            name=_validated_data['name'],
            latLng=_validated_data['latLng']
        )

        try:
            _pin = new_pin.save()
        except:
            return pin_errors('Something went wrong', 500)

        # return success message
        return pin_success(
            message='Pin added successfully',
            response_data={
                "pin": PinSchema().dump(_pin)
            },
            status_code=201
        )


class PinResource(Resource):
    """ PinList Resource
        PUT /pin/:pin_id
    """

    @authorize_app_access
    @validate_user()
    @validate_request()
    def put(self, pin_id):
        """ Update Pin """
        # get data from request body
        _data = request.get_json()
        
        # validate pin exists
        pin = Pins.get_by_id(pin_id)
        if not pin:
            return pin_errors('Pin does not exist', 400)

        # validate user owns pin
        if pin.user_id != g.current_user_id:
            return pin_errors('Unauthorized access', 401)

        # validate pin schema data to update
        pin_schema = PinInfoSchema()
        _validated_data = None

        try:
            _validated_data = pin_schema.load(_data)
        except ValidationError as err:
            return pin_errors(err.messages, 400)

        is_pin_updated = Pins.update(pin, **_validated_data)

        updated_pin = Pins.get_by_id(pin_id)

        if is_pin_updated:
            # return success message
            return pin_success(
                message='Pin updated successfully',
                response_data={
                    "pin": PinSchema().dump(updated_pin)
                },
                status_code=200
            )

        # return error message
        return pin_errors('Something went wrong', 500)
