from flask_restful import Api

# import controllers
from ..controllers import (
    SampleResource, UserSignUpResource
)

api = Api()

# add routes
api.add_resource(SampleResource, '/sample', '/sample/')

api.add_resource(UserSignUpResource, '/signup', '/signup/')
