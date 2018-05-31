""" Import app, unittest and json modules into the file """
from app import app
import unittest
import json


class TestRequestResource(unittest.TestCase):
    """ A class to perform tests for the Request Resource """

    def setUp(self):
        """
        Setup the app to be in testing mode and make it able to use test client
        """
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.data = {
            "dummy_request": {
                "title": "My first request",
                "location": "Roysambu, Nairobi",
                "request_type": "maintenance",
                "description": "Requests' description"
            },
            "user": {
                "username": "user1",
                "email": "user@gmail.com",
                "name": "User One",
                "password": "mysupersecret",
                "confirm_password": "mysupersecret",
            },
            "creds": {
                "username": "user1",
                "password": "mysupersecret"
            }
        }

    # def register_user(self):
    #     """ Create a new user and return them """
    #     self.client.post('/api/v1/auth/signup/', data=self.data.get('user1')

    # def authenticate_user(self):
    #     """ Login the newly created user and return them """
    #     return self.client.post(
    #         '/api/v1/auth/signin/', data=self.data.get('creds')
    #     # return response

    # def register_and_authenticate_user(self):
    #    # Register the user first.
    #     registered_user=self.register_user()
    #     self.assertEqual(registered_user.status_code, 201)

    #     # Log the user in.
    #     authenticated_user=self.authenticate_user()
    #     self.assertEqual(authenticated_user.status_code, 200)

    def test_get_requests(self):
        """ Test all resources can be successfully retrived """
        response = self.client.post(
            '/api/v1/users/requests/',
            data=json.dumps(self.data["dummy_request"]),
            content_type=("application/json")
        )

        self.assertEqual(response.status_code, 201)
        response = self.client.get('/api/v1/users/requests/')
        self.assertEqual(response.status_code, 200)

    def test_get_a_request(self):
        """ Test a resource can be successfully retrived """
        # self.register_and_authenticate_user()

        response = self.client.post(
            '/api/v1/users/requests/',
            data=json.dumps(self.data["dummy_request"]),
            content_type=("application/json")
        )
        self.assertEqual(response.status_code, 201)
        # created_resource = json.loads(response.data)
        response = self.client.get('/api/v1/users/request/1/')
        self.assertEqual(response.status_code, 200)

    def test_post_a_request(self):
        """ Test a resource can be successfully created"""
        response = self.client.post(
            '/api/v1/users/requests/',
            data=json.dumps(self.data["dummy_request"]),
            content_type=("application/json")
        )
        self.assertEqual(response.status_code, 201)

    def tests_empty_dict(self):
        response = self.client.post(
            'api/v1/users/requests/',
            data={},
            content_type=("application/json")
        )

        self.assertEqual(response.status_code, 400)

    def tests_empty_list(self):
        response = self.client.post(
            'api/v1/users/requests/',
            data=[],
            content_type=("application/json")
        )
        self.assertEqual(response.status_code, 400)

    def tests_empty_string(self):
        response = self.client.post(
            'api/v1/users/requests/',
            data="",
            content_type=("application/json")
        )
        self.assertEqual(response.status_code, 400)

    def tests_empty_tuple(self):
        response = self.client.post(
            'api/v1/users/requests/',
            data=(),
            content_type=("application/json")
        )
        self.assertEqual(response.status_code, 400)

    def tests_bad_data(self):
        response = self.client.post(
            'api/v1/users/requests/',
            data={
                "request_id": 1,
                'title': '',
                "location": 234
            },
            content_type=("application/json")
        )
        self.assertEqual(response.status_code, 400)

    def test_update_a_request(self):
        """ Test a resource can be successfully updated """
        response = self.client.post(
            '/api/v1/users/requests/',
            data=json.dumps(self.data["dummy_request"]),
            content_type=("application/json")
        )
        self.assertEqual(response.status_code, 201)

        response = self.client.put(
            '/api/v1/users/request/1/', data=json.dumps(dict(location="New title")), content_type=("application/json")
        )
        self.assertEqual(response.status_code, 200)

    def test_update_with_empty_dict(self):
        response = self.client.post(
            '/api/v1/users/requests/',
            data=json.dumps(self.data["dummy_request"]),
            content_type=("application/json")
        )

        self.assertEqual(response.status_code, 201)

        response = self.client.put(
            'api/v1/users/request/1/', data={},
            content_type="application/json")

        self.assertEqual(response.status_code, 400)

    def test_update_with_empty_list(self):
        response = self.client.post(
            '/api/v1/users/requests/',
            data=json.dumps(self.data["dummy_request"]),
            content_type=("application/json")
        )

        self.assertEqual(response.status_code, 201)

        response = self.client.put(
            'api/v1/users/request/1/', data=[],
            content_type="application/json")

        self.assertEqual(response.status_code, 400)

    def test_update_with_empty_string(self):
        response = self.client.post(
            '/api/v1/users/requests/',
            data=json.dumps(self.data["dummy_request"]),
            content_type=("application/json")
        )

        self.assertEqual(response.status_code, 201)

        response = self.client.put(
            'api/v1/users/request/1/', data="",
            content_type="application/json")

        self.assertEqual(response.status_code, 400)

    def test_update_with_empty_tuple(self):
        response = self.client.post(
            '/api/v1/users/requests/',
            data=json.dumps(self.data["dummy_request"]),
            content_type=("application/json")
        )

        self.assertEqual(response.status_code, 201)

        response = self.client.put(
            'api/v1/users/request/1/', data=(),
            content_type="application/json")

        self.assertEqual(response.status_code, 400)

    def test_update_with_bad_data(self):
        response = self.client.post(
            '/api/v1/users/requests/',
            data=json.dumps(self.data["dummy_request"]),
            content_type=("application/json")
        )

        self.assertEqual(response.status_code, 201)

        response = self.client.put(
            'api/v1/users/request/1/', data={
                "request_id": 1,
                'title': '',
                "location": 234,
            },
            content_type="application/json")

        self.assertEqual(response.status_code, 400)

    def test_delete_a_request(self):
        """ Test if a resource can be deleted successfully method """
        # self.register_and_authenticate_user()

        response = self.client.post(
            '/api/v1/users/requests/',
            data=json.dumps(self.data["dummy_request"]),
            content_type=("application/json")
        )
        self.assertEqual(response.status_code, 201)

        res = self.client.delete(
            '/api/v1/users/request/1/')
        self.assertEqual(res.status_code, 200)

        request_res = self.client.get('/api/v1/users/request/1/')
        self.assertEqual(request_res.status_code, 404)


if __name__ == '__main__':
    unittest.main()
