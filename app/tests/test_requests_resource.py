from app import app
import unittest


class TestRequestResource(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_get_request(self):
        response = self.client.get('api/v1/users/requests/')
        self.assertEqual(response.status_code, 200)

    def test_post_request(self):
        response = self.client.post('api/v1/users/requests/', data=dict(
            title="My first request",
            location="Roysambu, Nairobi",
            request_type="maintenance",
            descritption="Requests' description"
        ))

        self.assertEqual(response.status_code, 201)

    def test_update_request(self):
        response = self.client.put('api/v1/users/requests/1', data=dict(
            title="My first request",
            location="Roysambu, Nairobi",
            request_type="maintenance",
            descritption="Requests' description"
        ))

        self.assertEqual(response.status_code, 200)
