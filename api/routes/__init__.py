from flask_restful import Api

# import controllers
from ..controllers import (
    SampleResource, UserSignUpResource, UserLoginResource,
    UserResource, UserListResource
)

api = Api()

# add routes
api.add_resource(SampleResource, '/sample', '/sample/')

api.add_resource(UserSignUpResource, '/signup', '/signup/')
api.add_resource(UserLoginResource, '/login', '/login/')

api.add_resource(UserResource, '/user_info', '/user_info/')
api.add_resource(UserListResource, '/all_users', '/all_users/')
