from flask_restful import Api

# import controllers
from ..controllers import (
    SampleResource, UserSignUpResource, UserLoginResource,
    UserResource, UserListResource, PinListResource,
    PinResource
)

api = Api()

# add routes
api.add_resource(SampleResource, '/sample', '/sample/')

api.add_resource(UserSignUpResource, '/signup', '/signup/')
api.add_resource(UserLoginResource, '/login', '/login/')

api.add_resource(UserResource, '/user_info', '/user_info/')
api.add_resource(UserListResource, '/all_users', '/all_users/')

api.add_resource(PinListResource, '/pin', '/pin/')
api.add_resource(PinResource, '/pin/<string:pin_id>', '/pin/<string:pin_id>/')
