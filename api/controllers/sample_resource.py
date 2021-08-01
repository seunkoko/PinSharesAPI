import os

from flask import g, request
from flask_restful import Resource


class SampleResource(Resource):
    """ Sample Resource 
        GET /sample - Get imaginary sample api
    """

    def get(self):
        # return imaginary sample api
        return dict(
            status='success',
            data={
                'message': 'Successfully hit this endpoint',
            }
        ), 200
