import os
import json

from flask_testing import TestCase
from server import create_flask_app

from api.models import (
    db
)

from .default_test_data.default_data import (
    create_default_users, create_default_pins
)


class BaseTestCase(TestCase):
    """ Testing Setup """

    def create_app(self):
        """ Create app instance for testing """
        self.app = create_flask_app('testing')
        
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.secret_key = os.getenv('APP_SECRET')

        self.client = self.app.test_client()

        return self.app

    def setUp(self):
        """ Drop Database Table and Re-Create """
        db.drop_all()
        db.create_all()

    def tearDown(self):
        """ Drop Database Tables """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self, username, password):
        """ Login User """
        response = self.client.post('login',
            data=json.dumps({
                "username": username,
                "password": password
            }),
            content_type='application/json')

        response_data = json.loads(response.data)
        self.authorization_token = response_data["data"]["token"]

    def create_default_data(self):
        """ Create default data """
        create_default_users()
        create_default_pins()
