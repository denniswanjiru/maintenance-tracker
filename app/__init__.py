from flask import Flask
from flask_restful import Resource, Api, reqparse, abort

app = Flask(__name__)
api = Api(app)

requests = []

parser = reqparse.RequestParser()
parser.add_argument('title', required=True, type=str)
parser.add_argument('location', required=True, type=str)
parser.add_argument('request_type', required=True)
parser.add_argument('description')


class RequestList(Resource):
    def get(self):
        return {"requests": requests}, 200

    def post(self):
        args = parser.parse_args()
        _request = {
            "request_id": requests[-1]["request_id"] + 1 if requests else 1,
            "title": args['title'],
            "location": args['location'],
            "request_type": args['request_type'],
            "description": args['description']
        }
        requests.append(_request)
        return {"_request": _request}, 201


api.add_resource(RequestList, '/api/v1/users/requests/')
