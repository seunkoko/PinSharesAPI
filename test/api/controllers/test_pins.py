import json
import pytest

from test.base import BaseTestCase
from api.models import db, Users, Pins, PinShares


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


class PinTestCase(BaseTestCase):
    """ Test Update Pin """

    def setUp(self):
        db.drop_all()
        db.create_all()

        self.create_default_data() # create default data

        self.login('user1', 'password1') # login user1
        self.user1_token = self.authorization_token # user1's token

        self.login('user2', 'password2') # login user2
        self.user2_token = self.authorization_token # user2's token

        self.user1 = Users.find_first(**{'username': 'user1'}) # user1's info
        self.user2 = Users.find_first(**{'username': 'user2'}) # user2's info

        self.user1_pins = Pins.find_all(**{'user_id': self.user1.id}) # user1's pins
        self.user2_pins = Pins.find_all(**{'user_id': self.user2.id}) # user2's pins
    
    def test_update_pin_invalid_token(self):
        """ Test /pin/:pin_id
            - Update Pin with invalid token
        """
        response = self.client.put(
            'pin/{0}'.format(self.user1_pins[0].id),
            headers={'authorization': 'faketoken'},
            content_type='application/json'
        )
        response_data = json.loads(response.data)

        self.assertEqual(response_data['data']['message'],
            'Unauthorized. The authorization token supplied is invalid')
        self.assertEqual(response_data['status'], 'fail')
        self.assert401(response)

    def test_update_invalid_pin(self):
        """ Test /pin/:pin_id
            - Update Pin with invalid pin_id
        """
        response = self.client.put(
            'pin/{0}'.format('fakeid'),
            headers={'authorization': self.user1_token},
            data=json.dumps({"name": "updatedPinName"}),
            content_type='application/json'
        )
        response_data = json.loads(response.data)

        self.assertEqual(response_data['data']['message'],
            'Pin does not exist')
        self.assertEqual(response_data['status'], 'fail')
        self.assert400(response)

    def test_update_unauthorized_pin(self):
        """ Test /pin/:pin_id
            - Update Pin belonging to another user
        """
        response = self.client.put(
            'pin/{0}'.format(self.user2_pins[0].id),
            headers={'authorization': self.user1_token},
            data=json.dumps({"name": "updatedPinName"}),
            content_type='application/json'
        )
        response_data = json.loads(response.data)

        self.assertEqual(response_data['data']['message'],
            'Unauthorized access')
        self.assertEqual(response_data['status'], 'fail')
        self.assert401(response)

    def test_update_pin_invalid_latLng(self):
        """ Test /pin/:pin_id
            - Update Pin with invalid latLng
        """
        response = self.client.put(
            'pin/{0}'.format(self.user1_pins[0].id),
            headers={'authorization': self.user1_token},
            data=json.dumps({"latLng": ["0", "1", "2"]}),
            content_type='application/json'
        )
        response_data = json.loads(response.data)

        self.assertEqual(response_data['data']['message'],
            {'latLng': ['Length must be between 2 and 2.']})
        self.assertEqual(response_data['status'], 'fail')
        self.assert400(response)

    def test_update_pin_successful(self):
        """ Test /pin/:pin_id
            - Update Pin with valid token
        """
        response = self.client.put(
            'pin/{0}'.format(self.user1_pins[0].id),
            headers={'authorization': self.user1_token},
            data=json.dumps({"name": "updatedPinName"}),
            content_type='application/json'
        )
        response_data = json.loads(response.data)

        self.assertEqual(response_data['data']['message'],
            'Pin updated successfully')
        self.assertEqual(response_data['status'], 'success')
        self.assert200(response)


class SharePinTestCase(BaseTestCase):
    """ Test Share Pin """

    def setUp(self):
        db.drop_all()
        db.create_all()

        self.create_default_data() # create default data

        self.login('user1', 'password1') # login user1
        self.user1_token = self.authorization_token # user1's token

        self.login('user2', 'password2') # login user2
        self.user2_token = self.authorization_token # user2's token

        self.user1 = Users.find_first(**{'username': 'user1'}) # user1's info
        self.user2 = Users.find_first(**{'username': 'user2'}) # user2's info

        self.user1_pins = Pins.find_all(**{'user_id': self.user1.id}) # user1's pins
        self.user2_pins = Pins.find_all(**{'user_id': self.user2.id}) # user2's pins
    
    def test_share_pin_invalid_token(self):
        """ Test /share_pin/:pin_id
            - Share Pin with invalid token
        """
        response = self.client.post(
            'share_pin/{0}'.format(self.user1_pins[0].id),
            headers={'authorization': 'faketoken'},
            content_type='application/json'
        )
        response_data = json.loads(response.data)

        self.assertEqual(response_data['data']['message'],
            'Unauthorized. The authorization token supplied is invalid')
        self.assertEqual(response_data['status'], 'fail')
        self.assert401(response)

    def test_share_pin_invalid_userIDs(self):
        """ Test /share_pin/:pin_id
            - Share Pin with invalid user_ids
        """
        response = self.client.post(
            'share_pin/{0}'.format('fakeid'),
            headers={'authorization': self.user1_token},
            data=json.dumps({"user_ids": "1"}),
            content_type='application/json'
        )
        response_data = json.loads(response.data)

        self.assertEqual(response_data['data']['message'],
            {'user_ids': ['Not a valid list.']})
        self.assertEqual(response_data['status'], 'fail')
        self.assert400(response)

    def test_share_invalid_pin(self):
        """ Test /share_pin/:pin_id
            - Share Pin with invalid pin_id
        """
        response = self.client.post(
            'share_pin/{0}'.format('fakeid'),
            headers={'authorization': self.user1_token},
            data=json.dumps({"user_ids": ["1"]}),
            content_type='application/json'
        )
        response_data = json.loads(response.data)

        self.assertEqual(response_data['data']['message'],
            'Pin does not exist')
        self.assertEqual(response_data['status'], 'fail')
        self.assert400(response)

    def test_share_unauthorized_pin(self):
        """ Test /share_pin/:pin_id
            - Share Pin belonging to another user
        """
        response = self.client.post(
            'share_pin/{0}'.format(self.user2_pins[0].id),
            headers={'authorization': self.user1_token},
            data=json.dumps({"user_ids": [self.user2.id]}),
            content_type='application/json'
        )
        response_data = json.loads(response.data)

        self.assertEqual(response_data['data']['message'],
            'Unauthorized access')
        self.assertEqual(response_data['status'], 'fail')
        self.assert401(response)

    def test_share_pin_successful(self):
        """ Test /share_pin/:pin_id
            - Share Pin with valid token and data
        """
        new_share = PinShares.find_first(
            **{
                'pin_id': self.user1_pins[0].id,
                'shared_to': self.user2.id,
                'shared_by': self.user1.id
            }
        )
        self.assertFalse(new_share)

        response = self.client.post(
            'share_pin/{0}'.format(self.user1_pins[0].id),
            headers={'authorization': self.user1_token},
            data=json.dumps({"user_ids": [self.user2.id]}),
            content_type='application/json'
        )
        response_data = json.loads(response.data)

        new_share = PinShares.find_first(
            **{
                'pin_id': self.user1_pins[0].id,
                'shared_to': self.user2.id,
                'shared_by': self.user1.id
            }
        )

        self.assertEqual(response_data['data']['message'],
            'Pin shared successfully')
        self.assertEqual(response_data['status'], 'success')
        self.assertTrue(new_share)
        self.assert200(response)
