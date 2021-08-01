import json
import pytest

from test.base import BaseTestCase
from api.models import db


class UserrSignUpTestCase(BaseTestCase):
    """ Test User SignUp """

    def setUp(self):
        db.drop_all()
        db.create_all()

        self.create_default_data() # create default data
    
    def test_username_not_provided(self):
        """ Test /signup
            - Create User without username
        """
        new_user = {'password': 'password'}

        response = self.client.post('signup', data=json.dumps(new_user), content_type='application/json')
        response_data = json.loads(response.data)

        self.assertEqual(response_data['data']['message'],
            {'username': ['Username is required']})
        self.assertEqual(response_data['status'], 'fail')
        self.assert400(response)

    def test_password_not_provided(self):
        """ Test /signup
            - Create User without password
        """
        new_user = {'username': 'new name'}

        response = self.client.post('signup', data=json.dumps(new_user), content_type='application/json')
        response_data = json.loads(response.data)

        self.assertEqual(response_data['data']['message'],
            {'password': ['Password is required']})
        self.assertEqual(response_data['status'], 'fail')
        self.assert400(response)

    def test_user_already_exists(self):
        """ Test /signup
            - Create User with an already existing name
        """
        new_user = {'username': 'user1', 'password': 'password'}

        response = self.client.post('signup', data=json.dumps(new_user), content_type='application/json')
        response_data = json.loads(response.data)

        self.assertEqual(response_data['data']['message'],
            'Username already exists')
        self.assertEqual(response_data['status'], 'fail')
        self.assert400(response)

    def test_user_already_exists_case_insensitive(self):
        """ Test /signup
            - Create User with an already existing name, testing case sensitivity
        """
        new_user = {'username': 'USer1', 'password': 'password'}

        response = self.client.post('signup', data=json.dumps(new_user), content_type='application/json')
        response_data = json.loads(response.data)

        self.assertEqual(response_data['data']['message'],
            'Username already exists')
        self.assertEqual(response_data['status'], 'fail')
        self.assert400(response)

    def test_user_signup_successful(self):
        """ Test /signup
            - Create new User successfully
        """
        new_user = {'username': 'new user', 'password': 'newpassword'}

        response = self.client.post('signup', data=json.dumps(new_user), content_type='application/json')
        response_data = json.loads(response.data)

        self.assertEqual(response_data['data']['message'],
            'User signed up successfully')
        self.assertTrue(response_data['data']['token'])
        self.assertEqual(response_data['status'], 'success')
        self.assertEqual(response.status_code, 201)
