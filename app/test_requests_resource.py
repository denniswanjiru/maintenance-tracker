from app import app
import unittest


class TestRequestResource(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_get_requests(self):
        response = self.client.get('api/v1/users/requests/')
        self.assertEqual(response.status_code, 200)

    def test_get_a_request(self):
        response = self.client.get('api/v1/users/requests/1/')
        self.assertEqual(response.status_code, 200)

    def test_post_requests(self):
        response = self.client.post('api/v1/users/requests/', data=dict(
            request_id=1,
            title="My first request",
            location="Roysambu, Nairobi",
            request_type="maintenance",
            descritption="Requests' description"
        ))

        self.assertEqual(response.status_code, 201)

    def test_update_a_request(self):
        response = self.client.put('api/v1/users/requests/1/', data=dict(
            request_id=1,
            title="My first request",
            location="Roysambu, Nairobi",
            request_type="maintenance",
            descritption="Requests' description"
        ))

        self.assertEqual(response.status_code, 200)

    def test_delete_a_request(self):
        response = self.client.post('api/v1/users/requests/', data=dict(
            request_id=1,
            title="My first request",
            location="Roysambu, Nairobi",
            request_type="maintenance",
            descritption="Requests' description"
        ))

        self.assertEqual(response.status_code, 200)

        res = self.client.delete('api/v1/users/requests/1/')
        self.assertEqual(res.status_code, 200)

        request_res = self.client.get('api/v1/users/requests/1')
        self.assertEqual(request_res.status_code, 404)


if __name__ == '__main__':
    unittest.main()
