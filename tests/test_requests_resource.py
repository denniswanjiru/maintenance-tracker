""" Import app, unittest and json modules into the file """
from app import app
import unittest
import json


class TestRequestResource(unittest.TestCase):
    """ A class to perform tests for the Request Resource """

    def setUp(self):
        """ Setup the app to be in testing mode and make it able to use test client """
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

    def create_and_login_user(self):
        """ Login a user user """
        # First create a new user
        self.client.post(
            '/api/v1/users/auth/signup/',
            data=json.dumps(self.data["user"]),
            content_type=("application/json")
        )

        # Log the user in
        self.client.post(
            '/api/v1/users/auth/signin/',
            data=json.dumps(self.data["creds"]),
            content_type=("application/json")
        )

    def create_and_login_fake_user(self):
        """ Login a user user """
        # First create a new user
        self.client.post(
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

        # Log the user in
        self.client.post(
            '/api/v1/users/auth/signin/',
            data=json.dumps(dict(
                username="test_user",
                password="root"
            )),
            content_type=("application/json")
        )

    def test_get_requests(self):
        """ Test all resources can be successfully retrived """
        self.create_and_login_user()

        response = self.client.post(
            '/api/v1/users/requests/',
            data=json.dumps(self.data["dummy_request"]),
            content_type=("application/json")
        )

        response = self.client.get('/api/v1/users/requests/')
        self.assertEqual(response.status_code, 200)

    def test_get_a_request(self):
        """ Test a resource can be successfully retrived """
        self.create_and_login_user()

        response = self.client.post(
            '/api/v1/users/requests/',
            data=json.dumps(self.data["dummy_request"]),
            content_type=("application/json")
        )

        response = self.client.get('/api/v1/users/request/1/')
        self.assertEqual(response.status_code, 200)

        def test_get_a_non_existing_request(self):
            """ Test user tries to retrieve a noin-existing request """
            self.create_and_login_user()

            response = self.client.post(
                '/api/v1/users/requests/',
                data=json.dumps(self.data["dummy_request"]),
                content_type=("application/json")
            )

            response = self.client.get('/api/v1/users/request/1000/')
            self.assertEqual(response.status_code, 404)

    def test_post_a_request(self):
        """ Test a if resource can be successfully created """
        self.create_and_login_user()

        response = self.client.post(
            '/api/v1/users/requests/',
            data=json.dumps(self.data["dummy_request"]),
            content_type=("application/json")
        )

        self.assertEqual(response.status_code, 201)

    def tests_empty_dict(self):
        """ Test for empty dict bad data """
        self.create_and_login_user()

        response = self.client.post(
            'api/v1/users/requests/',
            data={},
            content_type=("application/json")
        )

        self.assertEqual(response.status_code, 400)

    def tests_empty_list(self):
        """ Test for empty list bad data """
        self.create_and_login_user()

        response = self.client.post(
            'api/v1/users/requests/',
            data=[],
            content_type=("application/json")
        )

        self.assertEqual(response.status_code, 400)

    def tests_empty_string(self):
        """ Test for empty string bad data """
        self.create_and_login_user()

        response = self.client.post(
            'api/v1/users/requests/',
            data="",
            content_type=("application/json")
        )

        self.assertEqual(response.status_code, 400)

    def tests_empty_tuple(self):
        """ Test for empty tuple bad data """
        self.create_and_login_user()

        response = self.client.post(
            'api/v1/users/requests/',
            data=(),
            content_type=("application/json")
        )

        self.assertEqual(response.status_code, 400)

    def tests_bad_data(self):
        """ Test for when user inputs bad data """
        self.create_and_login_user()

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
        self.create_and_login_user()

        self.client.post(
            '/api/v1/users/requests/',
            data=json.dumps(self.data["dummy_request"]),
            content_type=("application/json")
        )

        response = self.client.put(
            '/api/v1/users/request/1/',
            data=json.dumps(dict(location="New title")),
            content_type=("application/json")
        )

        self.assertEqual(response.status_code, 200)

    def test_update_with_empty_dict(self):
        """ Test for empty dict bad data  on update """
        self.create_and_login_user()

        self.client.post(
            '/api/v1/users/requests/',
            data=json.dumps(self.data["dummy_request"]),
            content_type=("application/json")
        )

        response = self.client.put(
            'api/v1/users/request/1/', data={},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)

    def test_update_with_empty_list(self):
        """ Test for empty list bad data  on update """
        self.create_and_login_user()

        self.client.post(
            '/api/v1/users/requests/',
            data=json.dumps(self.data["dummy_request"]),
            content_type=("application/json")
        )

        response = self.client.put(
            'api/v1/users/request/1/', data=[],
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)

    def test_update_with_empty_string(self):
        """ Test for empty string bad data  on update """
        self.create_and_login_user()

        self.client.post(
            '/api/v1/users/requests/',
            data=json.dumps(self.data["dummy_request"]),
            content_type=("application/json")
        )

        response = self.client.put(
            'api/v1/users/request/1/', data="",
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)

    def test_update_with_empty_tuple(self):
        """ Test for empty tuple bad data  on update """
        self.create_and_login_user()

        self.client.post(
            '/api/v1/users/requests/',
            data=json.dumps(self.data["dummy_request"]),
            content_type=("application/json")
        )

        response = self.client.put(
            'api/v1/users/request/1/', data=(),
            content_type="application/json")

        self.assertEqual(response.status_code, 400)

    def test_update_with_bad_data(self):
        """ Test for bad data  on update """
        self.create_and_login_user()

        self.client.post(
            '/api/v1/users/requests/',
            data=json.dumps(self.data["dummy_request"]),
            content_type=("application/json")
        )

        response = self.client.put(
            'api/v1/users/request/1/', data={
                "request_id": 1,
                'title': '',
                "location": 234,
            },
            content_type=("application/json")
        )

        self.assertEqual(response.status_code, 400)

    def test_z_delete_a_request(self):
        """ Test if a resource can be deleted successfully method """
        self.create_and_login_user()

        self.client.post(
            '/api/v1/users/requests/',
            data=json.dumps(self.data["dummy_request"]),
            content_type=("application/json")
        )

        respose = self.client.delete('/api/v1/users/request/1/')
        self.assertEqual(respose.status_code, 200)


if __name__ == '__main__':
    unittest.main()
