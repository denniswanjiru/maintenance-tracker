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
            "user": {
                "username": "user1",
                "email": "user@gmail.com",
                "name": "User One",
                "password": "mysupersecret",
                "confirm_password": "mysupersecret"
            },
            "creds": {
                "username": "user1",
                "password": "mysupersecret"
            }
        }

    def test_signin(self):
        """ Login a user user """
        # First create a new user
        response = self.client.post(
            '/api/v1/users/auth/signup/',
            data=json.dumps(self.data["user"]),
            content_type=("application/json")
        )
        self.assertEqual(response.status_code, 201)

        # Log the user in
        response = self.client.post(
            '/api/v1/users/auth/signin/',
            data=json.dumps(self.data["creds"]),
            content_type=("application/json")
        )
        self.assertEqual(response.status_code, 200)

    # def test_signup(self):
    #     """ Login a user user """
    #     # First create a new user
    #     response = self.client.post(
    #         '/api/v1/users/auth/signup/',
    #         data=json.dumps(self.data["user"]),
    #         content_type=("application/json")
    #     )
    #     self.assertEqual(response.status_code, 201)


if __name__ == '__main__':
    unittest.main()
