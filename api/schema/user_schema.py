from flask.json import dump
from marshmallow import Schema, fields, validate

from .pin_schema import PinSchema

class UserSchema(Schema):
    """ User Schema """

    id = fields.Str(dump_only=True)

    username = fields.Str(
        required=True,
        error_messages={'required': 'Username is required'},
        validate=[
            validate.Regexp(
                regex=r'^(?!\s*$)', error='Not a valid username.'
            )
        ]
    )

    password = fields.Str(
        load_only=True,
        required=True,
        error_messages={'required': 'Password is required'},
        validate=[
            validate.Regexp(
                regex=r'^(?!\s*$)', error='Not a valid password.'
            )
        ]
    )

    my_pins = fields.Nested(PinSchema, many=True, dump_only=True)

    is_active = fields.Boolean()

    created_at = fields.DateTime(dump_only=True)

    modified_at = fields.DateTime(dump_only=True)
