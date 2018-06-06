""" Import app, unittest and json modules into the file """
from app import app
import unittest
import json


class TestRequestResource(unittest.TestCase):
    """ A class to perform tests for the Request Resource """

    def setUp(self):
        """
        Setup the app to be in testing mode and
        make it able to use test client
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
            "user_login": {
                "username": "user2",
                "email": "user2@gmail.com",
                "name": "User One",
                "password": "mysupersecret",
                "confirm_password": "mysupersecret"
            },
            "creds_login": {
                "username": "user2",
                "password": "mysupersecret"
            }
        }

    def test_signup(self):
        """ Signup a user """
        response = self.client.post(
            '/api/v1/users/auth/signup/',
            data=json.dumps(self.data["user"]),
            content_type=("application/json")
        )

        self.assertEqual(response.status_code, 201)

    def test_signin(self):
        """ Signin a user """
        # First create a new user
        self.client.post(
            '/api/v1/users/auth/signup/',
            data=json.dumps(self.data["user_login"]),
            content_type=("application/json")
        )

        # Log the user in
        response = self.client.post(
            '/api/v1/users/auth/signin/',
            data=json.dumps(self.data["creds_login"]),
            content_type=("application/json")
        )

        self.assertEqual(response.status_code, 200)

    def test_signout(self):
        """Signout a user """
        # Sign the user out
        response = self.client.post('/api/v1/users/auth/signout/')
        self.assertEqual(response.status_code, 200)

    def test_username_taken(self):
        """ Test if the username is already taken """
        self.client.post(
            '/api/v1/users/auth/signup/',
            data=json.dumps(self.data["user"]),
            content_type=("application/json")
        )

        response = self.client.post(
            '/api/v1/users/auth/signup/',
            data=json.dumps(self.data["user"]),
            content_type=("application/json")
        )

        self.assertEqual(response.status_code, 400)

    def test_email_taken(self):
        """ Test if the email is already taken """
        self.client.post(
            '/api/v1/users/auth/signup/',
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
            '/api/v1/users/auth/signup/',
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
            '/api/v1/users/auth/signup/',
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

    def test_email_taken(self):
        """ Test if the email is already taken """
        self.client.post(
            '/api/v1/users/auth/signup/',
            data=json.dumps(dict(
                username="greater",
                email="greater@gmail.com",
                name="Dennis",
                password="root",
                confirm_password="root"
            )),
            content_type=("application/json")
        )

        response = self.client.post(
            '/api/v1/users/auth/signin/',
            data=json.dumps(dict(
                username="greater",
                password="wrong-password"
            )),
            content_type=("application/json")
        )

        self.assertEqual(response.status_code, 403)


if __name__ == '__main__':
    unittest.main()
