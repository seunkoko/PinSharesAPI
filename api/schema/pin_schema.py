from flask.json import dump
from marshmallow import Schema, fields, validate


class PinUserInfoSchema(Schema):
    """ User Info Schema 
        - minimal user info
    """
    id = fields.Str(dump_only=True)
    
    username = fields.Str(dump_only=True)


class PinInfoSchema(Schema):
    """ Pin Info Schema 
        - minimal pin info
    """
    name = fields.Str()

    latLng = fields.List(fields.Float(), validate=validate.Length(min=2,max=2))


class SharePinSchema(Schema):
    """ Share Pin Schema 
        - to validate share pin request
    """
    user_ids = fields.List(
        fields.Str(),
        validate=validate.Length(min=1, max=10),
        required=True
    )


class PinSchema(Schema):
    """ Pin Schema """
    id = fields.Str(dump_only=True)

    user_id = fields.Str(
        required=True,
        error_messages={'required': 'UserID is required'},
        validate=[
            validate.Regexp(
                regex=r'^(?!\s*$)', error='Not a valid user_id.'
            )
        ]
    )

    name = fields.Str(
        required=True,
        error_messages={'required': 'Pin name is required'},
        validate=[
            validate.Regexp(
                regex=r'^(?!\s*$)', error='Not a valid pin name.'
            )
        ]
    )

    latLng = fields.List(
        fields.Float(),
        required=True,
        validate=validate.Length(min=2,max=2)
    )

    user = fields.Nested(PinUserInfoSchema, dump_only=True)

    shared = fields.Boolean(dump_only=True)

    is_active = fields.Boolean()

    created_at = fields.DateTime(dump_only=True)

    modified_at = fields.DateTime(dump_only=True)



