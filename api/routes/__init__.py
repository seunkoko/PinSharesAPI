from flask_restful import Api

# import controllers
from ..controllers import (
    SampleResource, UserSignUpResource, UserLoginResource
)

api = Api()

# add routes
api.add_resource(SampleResource, '/sample', '/sample/')

api.add_resource(UserSignUpResource, '/signup', '/signup/')
api.add_resource(UserLoginResource, '/login', '/login/')
