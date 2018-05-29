from app import app
import unittest


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
        response = self.client.get('api/v1/users/requests/')
        self.assertEqual(response.status_code, 200)

    def test_get_a_request(self):
        response = self.client.get('api/v1/users/requests/1/')
        self.assertEqual(response.status_code, 200)

    def test_post_a_request(self):
        response = self.client.post(
            'api/v1/users/requests/', data=self.data["request"])

        self.assertEqual(response.status_code, 201)

    def test_400_post_requests(self):
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
        response = self.client.put(
            'api/v1/users/requests/1/', data=self.data["request"])

        self.assertEqual(response.status_code, 200)

    def test_delete_a_request(self):
        response = self.client.post(
            'api/v1/users/requests/', data=self.data["request"])

        self.assertEqual(response.status_code, 200)

        res = self.client.delete('api/v1/users/requests/1/')
        self.assertEqual(res.status_code, 200)

        request_res = self.client.get('api/v1/users/requests/1')
        self.assertEqual(request_res.status_code, 404)


if __name__ == '__main__':
    unittest.main()
