import json
import pytest

from test.base import BaseTestCase
from api.models import db, Users, Pins


class PinListTestCase(BaseTestCase):
    """ Test Add Pin """

    def setUp(self):
        db.drop_all()
        db.create_all()

        self.create_default_data() # create default data

        self.login('user1', 'password1') # login user1
        self.user1_token = self.authorization_token # user1's token

        self.user1 = Users.find_first(**{'username': 'user1'}) # user1's info

        self.user1_pins = Pins.find_all(**{'user_id': self.user1.id}) # user1's pins
    
    def test_add_pin_invalid_token(self):
        """ Test /pin
            - Create Pin with invalid token
        """
        response = self.client.post(
            'pin',
            headers={'authorization': 'faketoken'},
            content_type='application/json'
        )
        response_data = json.loads(response.data)

        self.assertEqual(response_data['data']['message'],
            'Unauthorized. The authorization token supplied is invalid')
        self.assertEqual(response_data['status'], 'fail')
        self.assert401(response)

    def test_add_pin_no_name(self):
        """ Test /pin
            - Create Pin with invalid name
        """
        response = self.client.post(
            'pin',
            headers={'authorization': self.user1_token},
            data=json.dumps({"latLng": [2, 3]}),
            content_type='application/json'
        )
        response_data = json.loads(response.data)

        self.assertEqual(response_data['data']['message'],
            {'name': ['Pin name is required']})
        self.assertEqual(response_data['status'], 'fail')
        self.assert400(response)

    def test_add_pin_no_latLng(self):
        """ Test /pin
            - Create Pin with no latLng value
        """
        response = self.client.post(
            'pin',
            headers={'authorization': self.user1_token},
            data=json.dumps({"name": "newPin"}),
            content_type='application/json'
        )
        response_data = json.loads(response.data)

        self.assertEqual(response_data['data']['message'],
            {'latLng': ['Missing data for required field.']})
        self.assertEqual(response_data['status'], 'fail')
        self.assert400(response)

    def test_add_pin_invalid_latLng(self):
        """ Test /pin
            - Create Pin with invalid latLng
        """
        response = self.client.post(
            'pin',
            headers={'authorization': self.user1_token},
            data=json.dumps({"name": "newPin", "latLng": ["0", "1", "2"]}),
            content_type='application/json'
        )
        response_data = json.loads(response.data)

        self.assertEqual(response_data['data']['message'],
            {'latLng': ['Length must be between 2 and 2.']})
        self.assertEqual(response_data['status'], 'fail')
        self.assert400(response)

    def test_add_pin_successful(self):
        """ Test /pin
            - Create Pin with valid token
        """
        response = self.client.post(
            'pin',
            headers={'authorization': self.user1_token},
            data=json.dumps({"name": "newPin", "latLng": [2, 3]}),
            content_type='application/json'
        )
        response_data = json.loads(response.data)

        self.assertEqual(response_data['data']['message'],
            'Pin added successfully')
        self.assertEqual(response_data['status'], 'success')
        self.assertEqual(response.status_code, 201) 
