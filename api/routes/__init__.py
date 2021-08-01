from flask_restful import Api

# import controllers
from ..controllers import (
    SampleResource
)

api = Api()

# add routes
api.add_resource(SampleResource, '/sample', '/sample/')
