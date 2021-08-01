from test.base import BaseTestCase


class TestMain(BaseTestCase):
    """ Dummy Test """

    def test_app_get(self):
        response = self.client.get('/')
        self.assert200(response)
