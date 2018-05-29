from app import app
import unittest


class TestRequestResource(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_get_request(self):
        response = self.client.get('api/v1/users/requests/')
        self.assertEqual(response.status_code, 200)
