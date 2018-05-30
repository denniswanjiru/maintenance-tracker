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
            "request": {
                "request_id": 1,
                "title": "My first request",
                "location": "Roysambu, Nairobi",
                "request_type": "maintenance",
                "descritption": "Requests' description"
            },
            "user1": {
                "username": "user1",
                "password": "mysupersecret",
                "email": "user@gmail.com",
                "name": "User One",
                "token": "SFNJFSD8IFSDI3CX8V9WVCXZ98FDSCSD8XCVZ32F"
            },
            "creds": {
                "username": "user1",
                "password": "mysupersecret"
            }
        }

    def register_user(self):
        """ Create a new user and return them """
        response = self.client.post(
            '/api/v1/auth/signup/', data=self.data.get('user1'), content_type="application/json")
        return response

    def authenticate_user(self):
        """ Login the newly created user and return them """
        response = self.client.post(
            '/api/v1/auth/signin/', data=self.data.get('creds'), content_type="application/json")
        return response

    def register_and_authenticate_user(self):
       # Register the user first.
        registered_user = self.register_user()
        self.assertEqual(registered_user.status_code, 201)

        # Log the user in.
        authenticated_user = self.authenticate_user()
        self.assertEqual(authenticated_user.status_code, 200)

    def test_get_requests(self):
        """ Test all resources can be successfully retrived """
        response = self.client.post(
            'api/v1/users/requests/',
            data=self.data["request"],
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        response = self.client.get(
            'api/v1/users/requests/', headers=self.token)
        self.assertEqual(response.status_code, 200)

    def test_get_a_request(self):
        """ Test a resource can be successfully retrived """
        self.register_and_authenticate_user()

        response = self.client.post(
            'api/v1/users/requests/',
            data=self.data["request"],
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        created_resource = json.loads(response.data)
        response = self.client.get(
            f'api/v1/users/requests/{created_resource["request_id"]}/', headers=self.token)
        self.assertEqual(response.status_code, 200)

    def test_post_a_request(self):
        """ Test a resource can be successfully created"""
        self.register_and_authenticate_user()

        response = self.client.post(
            'api/v1/users/requests/',
            data=self.data["request"],
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)

    def test_400_post_a_request(self):
        """ Test bad request on post method """
        self.register_and_authenticate_user()

        empty_dict = self.client.post(
            'api/v1/users/requests/', data={}, content_type="application/json")
        empty_tuple = self.client.post(
            'api/v1/users/requests/', data=(), content_type="application/json")
        empty_list = self.client.post(
            'api/v1/users/requests/', data=[], content_type="application/json")
        empty_string = self.client.post(
            'api/v1/users/requests/', data="", content_type="application/json")
        bad_data = self.client.post('api/v1/users/requests/', data={
            "request_id": 1,
            'title': '',
            "location": 234,
        }, content_type="application/json"
        )

        self.assertEqual(empty_dict.status_code, 400)
        self.assertEqual(empty_tuple.status_code, 400)
        self.assertEqual(empty_list.status_code, 400)
        self.assertEqual(empty_string.status_code, 400)
        self.assertEqual(bad_data.status_code, 400)

    def test_update_a_request(self):
        """ Test a resource can be successfully updated """
        self.register_and_authenticate_user()

        response = self.client.post(
            'api/v1/users/requests/', data=self.data["request"],
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        created_resource = json.loads(response.data)
        response = self.client.put(
            f'api/v1/users/requests/{created_resource["request_id"]}/', data={
                "title": "My Actual request",
                "request_type": "repair"
            },
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

    def test_400_update_a_request(self):
        """ Test bad request on put method """
        self.register_and_authenticate_user()

        response = self.client.post(
            'api/v1/users/requests/', data=self.data["request"],
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)

        created_resource = json.loads(response.data)

        empty_dict = self.client.put(
            f'api/v1/users/requests/{created_resource["request_id"]}/', data={},
            content_type="application/json")
        empty_tuple = self.client.put(
            f'api/v1/users/requests/{created_resource["request_id"]}/', data=(),
            content_type="application/json")
        empty_list = self.client.put(
            f'api/v1/users/requests/{created_resource["request_id"]}/', data=[],
            content_type="application/json")
        empty_string = self.client.put(
            f'api/v1/users/requests/{created_resource["request_id"]}/', data="",
            content_type="application/json")
        bad_data = self.client.put(f'api/v1/users/requests/{created_resource["request_id"]}/', data={
            "request_id": 1,
            'title': '',
            "location": 234,
        }, content_type="application/json")

        self.assertEqual(empty_dict.status_code, 400)
        self.assertEqual(empty_tuple.status_code, 400)
        self.assertEqual(empty_list.status_code, 400)
        self.assertEqual(empty_string.status_code, 400)
        self.assertEqual(bad_data.status_code, 400)

    def test_delete_a_request(self):
        """ Test if a resource can be deleted successfully method """
        self.register_and_authenticate_user()

        response = self.client.post(
            'api/v1/users/requests/', data=self.data["request"],
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)

        created_resource = json.loads(response.data)

        res = self.client.delete(
            f'api/v1/users/requests/{created_resource["request_id"]}/', headers=self.token)
        self.assertEqual(res.status_code, 200)

        request_res = self.client.get(
            f'api/v1/users/requests/{created_resource["request_id"]}/', headers=self.token)
        self.assertEqual(request_res.status_code, 404)


if __name__ == '__main__':
    unittest.main()
