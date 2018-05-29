
from app import app
import unittest
import json


class TestRequestResource(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.data = {
            "request": {
                "request_id": 1,
                "title": "My first request",
                "location": "Roysambu, Nairobi",
                "request_type": "maintenance",
                "descritption": "Requests' description"
            }
        }

    def test_get_requests(self):
        response = self.client.post(
            'api/v1/users/requests/', data=self.data["request"])
        self.assertEqual(response.status_code, 201)
        response = self.client.get('api/v1/users/requests/')
        self.assertEqual(response.status_code, 200)

    def test_get_a_request(self):
        response = self.client.post(
            'api/v1/users/requests/', data=self.data["request"])
        self.assertEqual(response.status_code, 201)
        created_resource = json.loads(response.data)
        response = self.client.get(
            f'api/v1/users/requests/{created_resource["request_id"]}/')
        self.assertEqual(response.status_code, 200)

    def test_post_a_request(self):
        response = self.client.post(
            'api/v1/users/requests/', data=self.data["request"])
        self.assertEqual(response.status_code, 201)

    def test_400_post_a_request(self):
        empty_dict = self.client.post('api/v1/users/requests/', data={})
        empty_tuple = self.client.post('api/v1/users/requests/', data=())
        empty_list = self.client.post('api/v1/users/requests/', data=[])
        empty_string = self.client.post('api/v1/users/requests/', data="")
        bad_data = self.client.post('api/v1/users/requests/', data={
            "request_id": 1,
            'title': '',
            "location": 234,
        })

        self.assertEqual(empty_dict.status_code, 400)
        self.assertEqual(empty_tuple.status_code, 400)
        self.assertEqual(empty_list.status_code, 400)
        self.assertEqual(empty_string.status_code, 400)
        self.assertEqual(bad_data.status_code, 400)

    def test_update_a_request(self):
        response = self.client.post(
            'api/v1/users/requests/', data=self.data["request"])
        self.assertEqual(response.status_code, 201)
        created_resource = json.loads(response.data)
        response = self.client.put(
            f'api/v1/users/requests/{created_resource["request_id"]}/', data={
                "title": "My Actual request",
                "request_type": "repair"
            })
        self.assertEqual(response.status_code, 200)

    def test_400_update_a_request(self):
        response = self.client.post(
            'api/v1/users/requests/', data=self.data["request"])
        self.assertEqual(response.status_code, 201)

        created_resource = json.loads(response.data)

        empty_dict = self.client.put(
            f'api/v1/users/requests/{created_resource["request_id"]}/', data={})
        empty_tuple = self.client.put(
            f'api/v1/users/requests/{created_resource["request_id"]}/', data=())
        empty_list = self.client.put(
            f'api/v1/users/requests/{created_resource["request_id"]}/', data=[])
        empty_string = self.client.put(
            f'api/v1/users/requests/{created_resource["request_id"]}/', data="")
        bad_data = self.client.put(f'api/v1/users/requests/{created_resource["request_id"]}/', data={
            "request_id": 1,
            'title': '',
            "location": 234,
        })

        self.assertEqual(empty_dict.status_code, 400)
        self.assertEqual(empty_tuple.status_code, 400)
        self.assertEqual(empty_list.status_code, 400)
        self.assertEqual(empty_string.status_code, 400)
        self.assertEqual(bad_data.status_code, 400)

    def test_delete_a_request(self):
        response = self.client.post(
            'api/v1/users/requests/', data=self.data["request"])

        self.assertEqual(response.status_code, 201)

        created_resource = json.loads(response.data)

        res = self.client.delete(
            f'api/v1/users/requests/{created_resource["request_id"]}/')
        self.assertEqual(res.status_code, 200)

        request_res = self.client.get(
            f'api/v1/users/requests/{created_resource["request_id"]}/',)
        self.assertEqual(request_res.status_code, 404)


if __name__ == '__main__':
    unittest.main()
