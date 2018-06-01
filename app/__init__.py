from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)

requests_store = []
users = {}

parser = reqparse.RequestParser()
parser.add_argument('title', required=True, type=str)
parser.add_argument('location', required=True, type=str)
parser.add_argument('request_type', required=True)
parser.add_argument('description')


def find_request(request_id):
    """ Find a specific request resource based off the id """
    return [_request for _request in requests_store if _request['request_id'] == request_id]


class RequestList(Resource):
    def get(self):
        return {"requests": requests_store}, 200

    def post(self):
        args = parser.parse_args()
        _request = {
            "request_id": requests_store[-1]["request_id"] + 1 if requests_store else 1,
            "title": args['title'],
            "location": args['location'],
            "request_type": args['request_type'],
            "description": args['description']
        }
        requests_store.append(_request)
        return {"request": _request}, 201


class Request(Resource):
    def get(self, request_id):
        """ Get a single request resource based off its id """
        _request = find_request(request_id)
        if len(_request) == 0:
            return {"message": f"request {request_id} doesn't exit."}, 404
        return {'request': _request[0]}, 200

    def put(self, request_id):
        """ Update a single request resource based off its id """
        data = request.get_json()
        _request = find_request(request_id)
        if len(_request) == 0:
            return {"message": f"request {request_id} doesn't exit."}, 404
        _request[0]['title'] = data.get('title', _request[0]['title'])
        _request[0]['location'] = data.get('location', _request[0]['location'])
        _request[0]['request_type'] = data.get(
            'request_type', _request[0]['request_type'])
        _request[0]['description'] = data.get(
            'description', _request[0]['description'])

        return {"requests": requests_store}, 200

    def delete(self, request_id):
        """ Delete a single request resource based off its id """
        _request = find_request(request_id)
        if len(_request) == 0:
            return {"message": f"request {request_id} doesn't exit."}, 404
        requests_store.remove(_request[0])
        return {"requests": requests_store}


class UserRegistration(Resource):
    def post(self):
        data = request.get_json()
        username_taken = [
            username for username in users if data["username"] in users]
        emails = [users[user]["email"] for user in users]

        if username_taken:
            return {"message": "username already taken"}, 400
        elif data["email"] in emails:
            return {"message": "email already taken"}, 400
        elif data["password"] != data["confirm_password"]:
            return {"message": "password and confirm_password fields do not match"}, 400

        users.update({
            data.get("username"): {
                "name": data.get("name"),
                "email": data.get("email"),
                "password": data.get("password")
            }
        })

        return {"users": users}, 201


class UserSignin(Resource):
    def post(self):
        data = request.get_json()
        username = data["username"]
        password = data["password"]

        if username in users:
            if users[username]["password"] != password:
                return {"message": "username or password do not match."}, 403
            return {"message": f"you are now logged in as {username}"}, 200
        return {"message": f"{username} does not have an account."}, 404


api.add_resource(RequestList, '/api/v1/users/requests/')
api.add_resource(Request, '/api/v1/users/request/<int:request_id>/')
api.add_resource(UserRegistration, '/api/v1/users/auth/signup/')
api.add_resource(UserSignin, '/api/v1/users/auth/signin/')
