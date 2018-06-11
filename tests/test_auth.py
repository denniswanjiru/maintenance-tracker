""" Import app, unittest and json modules into the file """
from app import app
import unittest
import json
from config import app_config
from db import init, drop


class TestRequestResource(unittest.TestCase):
    """ A class to perform tests for the Request Resource """

    def setUp(self):
        """
        Setup the app to be in testing mode and
        make it able to use test client
        """
        self.app = app
        self.app.config.from_object(app_config['testing'])
        self.app_context = self.app.app_context()
        self.app_context.push()
        init()
        self.client = self.app.test_client()
        self.data = {
            "user": {
                "username": "user1",
                "email": "user@gmail.com",
                "name": "User One",
                "password": "My_supersecret1",
                "confirm_password": "My_supersecret1"
            },
            "user_login": {
                "username": "user2",
                "email": "user2@gmail.com",
                "name": "User One",
                "password": "My_supersecret1",
                "confirm_password": "My_supersecret1"
            },
            "creds_login": {
                "username": "user2",
                "password": "My_supersecret1"
            }
        }

    def tearDown(self):
        drop()

    def test_signup(self):
        """ Signup a user """
        response = self.client.post(
            '/api/v2/users/auth/signup/',
            data=json.dumps(self.data["user"]),
            content_type=("application/json")
        )

        self.assertEqual(response.status_code, 201)

    def test_signin(self):
        """ Signin a user """
        # First create a new user
        self.client.post(
            '/api/v2/users/auth/signup/',
            data=json.dumps(self.data["user_login"]),
            content_type=("application/json")
        )

        # Log the user in
        response = self.client.post(
            '/api/v2/users/auth/signin/',
            data=json.dumps(self.data["creds_login"]),
            content_type=("application/json")
        )

        self.assertEqual(response.status_code, 200)

    # def test_signout(self):
    #     """Signout a user """
    #     # Sign the user out
    #     response = self.client.post('/api/v2/users/auth/signout/')
    #     self.assertEqual(response.status_code, 200)

    def test_username_taken(self):
        """ Test if the username is already taken """
        self.client.post(
            '/api/v2/users/auth/signup/',
            data=json.dumps(self.data["user"]),
            content_type=("application/json")
        )

        response = self.client.post(
            '/api/v2/users/auth/signup/',
            data=json.dumps(self.data["user"]),
            content_type=("application/json")
        )

        self.assertEqual(response.status_code, 400)

    def test_email_taken(self):
        """ Test if the email is already taken """
        self.client.post(
            '/api/v2/users/auth/signup/',
            data=json.dumps(dict(
                username="dennis",
                email="user1@gmail.com",
                name="Dennis",
                password="root",
                confirm_password="root"
            )),
            content_type=("application/json")
        )

        response = self.client.post(
            '/api/v2/users/auth/signup/',
            data=json.dumps(dict(
                username="creez",
                email="user1@gmail.com",
                name="Dennis",
                password="root",
                confirm_password="root"
            )),
            content_type=("application/json")
        )

        self.assertEqual(response.status_code, 400)

    def test_password_missmatch(self):
        """ Test if the email is already taken """
        response = self.client.post(
            '/api/v2/users/auth/signup/',
            data=json.dumps(dict(
                username="test_user",
                email="dennis@gmail.com",
                name="Dennis",
                password="root",
                confirm_password="rooter"
            )),
            content_type=("application/json")
        )

        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
