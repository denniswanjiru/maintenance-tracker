from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort

app = Flask(__name__)
api = Api(app)

requests_store = []

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
        _request = find_request(request_id)
        if len(_request) == 0:
            return {"message": f"request {request_id} doesn't exit."}, 404
        _request[0]['title'] = request.json.get(
            'title', _request[0]['title'])
        _request[0]['location'] = request.json.get(
            'location', _request[0]['location'])
        _request[0]['request_type'] = request.json.get(
            'request_type', _request[0]['request_type'])
        _request[0]['description'] = request.json.get(
            'description', _request[0]['description'])

        return {"requests": requests_store}

    def delete(self, request_id):
        """ Delete a single request resource based off its id """
        _request = find_request(request_id)
        if len(_request) == 0:
            return {"message": f"request {request_id} doesn't exit."}, 404
        requests_store.remove(_request[0])
        return {"requests": requests_store}


api.add_resource(RequestList, '/api/v1/users/requests/')
api.add_resource(Request, '/api/v1/users/request/<int:request_id>/')
