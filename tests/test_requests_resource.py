""" Import app, unittest and json modules into the file """
from app import app
import unittest
import json
from config import app_config
from db import init, drop


class TestRequestResource(unittest.TestCase):
    """ A class to perform tests for the Request Resource """

    def setUp(self):
        """ Setup the app to be in testing mode and make it able to use test client """
        self.app = app
        self.app.config.from_object(app_config['testing'])
        self.app_context = self.app.app_context()
        self.app_context.push()
        init()

        self.client = self.app.test_client()
        self.data = {
            "dummy_request": {
                "title": "My first request",
                "location": "Roysambu Nairobi",
                "request_type": "maintenance",
                "description": "Requests description"
            },
            "user": {
                "username": "user1",
                "email": "user@gmail.com",
                "name": "User One",
                "password": "My_supersecret1",
                "confirm_password": "My_supersecret1",
            },
            "creds": {
                "username": "user1",
                "password": "My_supersecret1"
            }
        }

    def tearDown(self):
        drop()

    def make_request(self, token):
        return self.client.post(
            '/api/v2/users/requests/',
            data=json.dumps(self.data["dummy_request"]),
            headers=dict(Authorization=f'Bearer {token}'),
            content_type=("application/json")
        )

    def create_and_login_user(self):
        """ Login a user user """
        # First create a new user
        res = self.client.post(
            '/api/v2/users/auth/signup/',
            data=json.dumps(self.data["user"]),
            content_type=("application/json")
        )

        print(res.data)

        # Log the user in
        res = self.client.post(
            '/api/v2/users/auth/signin/',
            data=json.dumps(self.data["creds"]),
            content_type=("application/json")
        )

        token = json.loads(res.data).get('access_token')
        return token

    def create_and_login_fake_user(self):
        """ Login a user user """
        # First create a new user
        self.client.post(
            '/api/v2/users/auth/signup/',
            data=json.dumps(dict(
                username="test_user",
                email="dennis@gmail.com",
                name="Dennis",
                password="Rooter_1",
                confirm_password="Rooter_1"
            )),
            content_type=("application/json")
        )

        # Log the user in
        res = self.client.post(
            '/api/v2/users/auth/signin/',
            data=json.dumps(dict(
                username="test_user",
                password="Rooter_1"
            )),
            content_type=("application/json")
        )

        token = json.loads(res.data).get('access_token')
        return token

    def test_get_requests(self):
        """ Test all resources can be successfully retrived """
        token = self.create_and_login_user()
        print(token)
        response = self.make_request(token)
        print(response.data)

        response = self.client.get(
            '/api/v2/users/requests/',
            headers=dict(Authorization=f'Bearer {token}')
        )
        print(response.data)
        self.assertEqual(response.status_code, 200)

    def test_get_a_request(self):
        """ Test a resource can be successfully retrived """
        token = self.create_and_login_user()

        response = self.make_request(token)

        response = self.client.get(
            '/api/v2/users/requests/',
            headers=dict(Authorization=f'Bearer {token}')
        )
        public_id = json.loads(response.data)["requests"][0]["public_id"]
        response = self.client.get(
            f'/api/v2/users/request/{public_id}/',
            headers=dict(Authorization=f'Bearer {token}')
        )

        self.assertEqual(response.status_code, 200)

    def test_get_a_non_existing_request(self):
        """ Test user tries to retrieve a noin-existing request """
        token = self.create_and_login_user()

        response = self.make_request(token)

        response = self.client.get(
            '/api/v2/users/request/2132435465sew/',
            headers=dict(Authorization=f'Bearer {token}')
        )

        self.assertEqual(response.status_code, 404)

    def test_not_users_request(self):
        """ Test a user tries to retrieve a post that don't belong to them """
        token1 = self.create_and_login_user()
        self.make_request(token1)
        response = self.client.get(
            '/api/v2/users/requests/',
            headers=dict(Authorization=f'Bearer {token1}')
        )
        public_id = json.loads(response.data)["requests"][0]["public_id"]
        token2 = self.create_and_login_fake_user()
        print(token2)
        response = self.client.get(
            f'/api/v2/users/request/{public_id}/',
            headers=dict(Authorization=f'Bearer {token2}'))
        print(response.data)
        self.assertEqual(response.status_code, 403)

    def test_post_a_request(self):
        """ Test a if resource can be successfully created """
        token = self.create_and_login_user()

        response = self.make_request(token)

        self.assertEqual(response.status_code, 201)

    def tests_empty_dict(self):
        """ Test for empty dict bad data """
        token = self.create_and_login_user()

        response = self.client.post(
            'api/v2/users/requests/',
            data={},
            headers=dict(Authorization=f'Bearer {token}'),
            content_type=("application/json")
        )

        self.assertEqual(response.status_code, 400)

    def tests_empty_list(self):
        """ Test for empty list bad data """
        token = self.create_and_login_user()

        response = self.client.post(
            'api/v2/users/requests/',
            data=[],
            headers=dict(Authorization=f'Bearer {token}'),
            content_type=("application/json")
        )

        self.assertEqual(response.status_code, 400)

    def tests_empty_string(self):
        """ Test for empty string bad data """
        token = self.create_and_login_user()

        response = self.client.post(
            'api/v2/users/requests/',
            data="",
            headers=dict(Authorization=f'Bearer {token}'),
            content_type=("application/json")
        )

        self.assertEqual(response.status_code, 400)

    def tests_empty_tuple(self):
        """ Test for empty tuple bad data """
        token = self.create_and_login_user()

        response = self.client.post(
            'api/v2/users/requests/',
            data=(),
            headers=dict(Authorization=f'Bearer {token}'),
            content_type=("application/json")
        )

        self.assertEqual(response.status_code, 400)

    def tests_bad_data(self):
        """ Test for when user inputs bad data """
        token = self.create_and_login_user()

        response = self.client.post(
            'api/v2/users/requests/',
            data={
                "request_id": 1,
                'title': '',
                "location": 234
            },
            headers=dict(Authorization=f'Bearer {token}'),
            content_type=("application/json")
        )

        self.assertEqual(response.status_code, 400)

    def test_update_a_request(self):
        """ Test a resource can be successfully updated """
        token = self.create_and_login_user()

        res = self.make_request(token)
        public_id = json.loads(res.data)['request']['public_id']

        response = self.client.put(
            f'/api/v2/users/request/{public_id}/',
            data=json.dumps(dict(location="New title")),
            headers=dict(Authorization=f'Bearer {token}'),
            content_type=("application/json")
        )

        self.assertEqual(response.status_code, 200)

    def test_update_with_empty_dict(self):
        """ Test for empty dict bad data  on update """
        token = self.create_and_login_user()

        res = self.make_request(token)
        public_id = json.loads(res.data)['request']['public_id']

        response = self.client.put(
            f'api/v2/users/request/{public_id}/', data={},
            headers=dict(Authorization=f'Bearer {token}'),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)

    def test_update_with_empty_list(self):
        """ Test for empty list bad data  on update """
        token = self.create_and_login_user()

        res = self.make_request(token)
        public_id = json.loads(res.data)['request']['public_id']

        response = self.client.put(
            f'api/v2/users/request/{public_id}/', data=[],
            headers=dict(Authorization=f'Bearer {token}'),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)

    def test_update_with_empty_string(self):
        """ Test for empty string bad data  on update """
        token = self.create_and_login_user()

        res = self.make_request(token)
        public_id = json.loads(res.data)['request']['public_id']

        response = self.client.put(
            f'api/v2/users/request/{public_id}/', data="",
            headers=dict(Authorization=f'Bearer {token}'),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)

    def test_update_with_empty_tuple(self):
        """ Test for empty tuple bad data  on update """
        token = self.create_and_login_user()

        res = self.make_request(token)
        public_id = json.loads(res.data)['request']['public_id']

        response = self.client.put(
            f'api/v2/users/request/{public_id}/', data=(),
            headers=dict(Authorization=f'Bearer {token}'),
            content_type="application/json")

        self.assertEqual(response.status_code, 400)

    def test_update_with_bad_data(self):
        """ Test for bad data  on update """
        token = self.create_and_login_user()

        res = self.make_request(token)
        public_id = json.loads(res.data)['request']['public_id']

        response = self.client.put(
            f'api/v2/users/request/{public_id}/', data={
                "request_id": 1,
                'title': '',
                "location": 234,
            },
            headers=dict(Authorization=f'Bearer {token}'),
            content_type=("application/json")
        )

        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
