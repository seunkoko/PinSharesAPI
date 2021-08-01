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


class UserLoginTestCase(BaseTestCase):
    """ Test User Login """

    def setUp(self):
        db.drop_all()
        db.create_all()

        self.create_default_data()
    
    def test_username_not_provided(self):
        """ Test /login
            - Login User without username
        """
        user = {'password': 'password1'}

        response = self.client.post('login', data=json.dumps(user), content_type='application/json')
        response_data = json.loads(response.data)

        self.assertEqual(response_data['data']['message'],
            {'username': ['Username is required']})
        self.assertEqual(response_data['status'], 'fail')
        self.assert400(response)

    def test_password_not_provided(self):
        """ Test /login
            - Login User without password
        """
        user = {'username': 'user1'}

        response = self.client.post('login', data=json.dumps(user), content_type='application/json')
        response_data = json.loads(response.data)

        self.assertEqual(response_data['data']['message'],
            {'password': ['Password is required']})
        self.assertEqual(response_data['status'], 'fail')
        self.assert400(response)

    def test_user_does_not_exist(self):
        """ Test /login
            - Login with invalid user details
        """
        user = {'username': 'user4', 'password': 'password'}

        response = self.client.post('login', data=json.dumps(user), content_type='application/json')
        response_data = json.loads(response.data)

        self.assertEqual(response_data['data']['message'],
            'Invalid username or password')
        self.assertEqual(response_data['status'], 'fail')
        self.assert400(response)

    def test_user_password_incorrect(self):
        """ Test /login
            - Login with invalid password
        """
        user = {'username': 'user1', 'password': 'password'}

        response = self.client.post('login', data=json.dumps(user), content_type='application/json')
        response_data = json.loads(response.data)

        self.assertEqual(response_data['data']['message'],
            'Invalid username or password')
        self.assertEqual(response_data['status'], 'fail')
        self.assert400(response)

    def test_user_login_successful(self):
        """ Test /login
            - Login user successful
        """
        user = {'username': 'user1', 'password': 'password1'}

        response = self.client.post('login', data=json.dumps(user), content_type='application/json')
        response_data = json.loads(response.data)

        self.assertEqual(response_data['data']['message'],
            'User login successful')
        self.assertTrue(response_data['data']['token'])
        self.assertEqual(response_data['status'], 'success')
        self.assert200(response)

    def test_user_login_name_case_insenstive(self):
        """ Test /login
            - Login user successful
            - Test case insensitivity
        """
        user = {'username': 'USer1', 'password': 'password1'}

        response = self.client.post('login', data=json.dumps(user), content_type='application/json')
        response_data = json.loads(response.data)

        self.assertEqual(response_data['data']['message'],
            'User login successful')
        self.assertTrue(response_data['data']['token'])
        self.assertEqual(response_data['status'], 'success')
        self.assert200(response)


class UserInfoTestCase(BaseTestCase):
    """ Test User Info """

    def setUp(self):
        db.drop_all()
        db.create_all()

        self.create_default_data()
    
    def test_get_user_info_invalid_token(self):
        """ Test /user_info
            - Get user info with invalid token
        """
        response = self.client.get(
            'user_info',
            headers={'authorization': 'faketoken'},
            content_type='application/json'
        )
        response_data = json.loads(response.data)

        self.assertEqual(response_data['data']['message'],
            'Unauthorized. The authorization token supplied is invalid')
        self.assertEqual(response_data['status'], 'fail')
        self.assert401(response)

    def test_fetch_user_info_successful(self):
        """ Test /user_info
            - Get user info with valid token
        """
        self.login('user1', 'password1')
        response = self.client.get(
            'user_info',
            headers={'authorization': self.authorization_token},
            content_type='application/json'
        )
        response_data = json.loads(response.data)

        self.assertEqual(response_data['data']['message'],
            'User info fetched successfully')
        self.assertEqual(response_data['status'], 'success')
        self.assertTrue(response_data['data']['user']['my_pins'])
        self.assertTrue(response_data['data']['user']['all_pins'])
        self.assertEqual(response_data['data']['user']['shares'], [])
        self.assert200(response)


class UserListTestCase(BaseTestCase):
    """ Test All Users """

    def setUp(self):
        db.drop_all()
        db.create_all()

        self.create_default_data()
    
    def test_get_user_info_invalid_token(self):
        """ Test /all_users
            - Get all users with valid token
        """
        response = self.client.get(
            'all_users',
            headers={'authorization': 'faketoken'},
            content_type='application/json'
        )
        response_data = json.loads(response.data)

        self.assertEqual(response_data['data']['message'],
            'Unauthorized. The authorization token supplied is invalid')
        self.assertEqual(response_data['status'], 'fail')
        self.assert401(response)

    def test_fetch_users_successful(self):
        """ Test /all_users
            - Get all users with valid token
        """
        self.login('user1', 'password1')
        response = self.client.get(
            'all_users',
            headers={'authorization': self.authorization_token},
            content_type='application/json'
        )
        response_data = json.loads(response.data)

        self.assertEqual(response_data['data']['message'],
            'Users fetched successfully')
        self.assertEqual(response_data['status'], 'success')
        self.assertTrue(response_data['data']['users'])
        self.assertEqual(len(response_data['data']['users']), 2)
        self.assert200(response)
