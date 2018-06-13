from flask import Flask, request, render_template

from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import (
    jwt_required, JWTManager, create_access_token, get_jwt_identity,
    jwt_refresh_token_required, create_refresh_token
)
from .models import User, Request as RequestModel

import os
import re

from config import app_config

app = Flask(__name__)

MODE = os.getenv('MODE') if os.getenv('MODE') else 'development'
app.config.from_object(app_config[MODE])
jwt = JWTManager(app)
api = Api(app)


def validate_str_field(string, name):
    if len(string.strip()) == 0:
        return {"message": f"{name} can't have empty values"}, 400
    elif not re.match("^[ A-Za-z0-9_-]*$", string):
        return {"message": f"{name} invalid datas"}, 400
    return None


def validate_username(string, name):
    if len(string.strip()) == 0:
        return {"message": f"{name} can't have empty values"}, 400
    elif not re.match("^[A-Za-z0-9_-]*$", string):
        return {"message": f"{name} should only contain letters, numbers, underscores and dashes"}, 400
    return None


@app.route('/')
def index():
    return render_template('index.html')


class RequestList(Resource):
    """ Resource for list request """

    parser = reqparse.RequestParser()
    parser.add_argument('title', required=True, type=str,
                        help="Required and must be a string")
    parser.add_argument('location', required=True, type=str)
    parser.add_argument('request_type', required=True)
    parser.add_argument('description')

    @jwt_required
    def get(self):
        """ Get all request """
        user = get_jwt_identity()
        request = RequestModel()

        my_requests = request.fetch_by_user(user["id"])

        if my_requests:
            return {"requests": my_requests}, 200
        return {"message": "You don't have any requests yet"}, 404

    @jwt_required
    def post(self):
        """ Create a new request """
        user = get_jwt_identity()
        args = RequestList.parser.parse_args()
        if validate_str_field(args["title"], 'Title'):
            return validate_str_field(args["title"], 'Title')
        elif validate_str_field(args["location"], 'location'):
            return validate_str_field(args["location"], 'location')
        elif validate_str_field(args["request_type"], 'request_type'):
            return validate_str_field(args["request_type"], 'request_type')

        _request = RequestModel(
            user_id=user["id"], title=args['title'], location=args['location'],
            request_type=args['request_type'], description=args['description']
        )

        _request.add()

        _request = _request.fetch_by_id(_request.public_id)

        return {"request": _request}, 201


class Request(Resource):
    """ Requests Resource """

    @jwt_required
    def get(self, request_id):
        """ Get a single request resource based off its id """
        user = get_jwt_identity()
        req = RequestModel()
        _request = req.fetch_by_id(request_id)

        if not _request:
            return {"message": f"request {request_id} doesn't exit."}, 404
        elif _request["user_id"] != user["id"]:
            return {"message": "You can only view your own requests"}, 403
        return {'request': _request}, 200

    @jwt_required
    def put(self, request_id):
        """ Update a single request resource based off its id """
        user = get_jwt_identity()
        data = request.get_json()
        req = RequestModel()
        _request = req.fetch_by_id(request_id)

        if not _request:
            return {"message": f"request {request_id} doesn't exit."}, 404
        elif _request['user_id'] != user["id"]:
            return {"message": "You can only edit your own requests"}, 403
        elif _request["status"] != 'pending':
            return {"message": "You can only update a pending request"}, 403
        elif data.get('status'):
            return {"message": "You can't change the status of your own requests"}, 403

        title = data.get('title', _request["title"])
        location = data.get('location', _request["location"])
        request_type = data.get('request_type', _request["request_type"])
        description = data.get('description', _request["description"])

        req = RequestModel(
            title=title, location=location, request_type=request_type,
            description=description)

        _request = req.update(request_id)
        updated_request = req.fetch_by_id(request_id)
        return {"request": updated_request}, 200

    @jwt_required
    def delete(self, request_id):
        """ Delete a single request resource based off its id """
        user = get_jwt_identity()
        req = RequestModel()
        _request = req.fetch_by_id(request_id)
        print(_request)
        print(user["id"])
        if not _request:
            return {"message": f"request {request_id} doesn't exit."}, 404
        elif _request["user_id"] != user["id"]:
            return {"message": "You can only delete your own requests"}, 403
        elif _request["status"] != 'pending':
            return {"message": "You can only delete a non-approved request"}, 403
        req.delete(_request["public_id"])
        return {"message": "Your request was successfully deleted"}, 200


class AdminRequests(Resource):
    """ View all the request """
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()

        if current_user["is_admin"]:
            req = RequestModel()
            _requests = req.fetch_all()
            return {"requests": _requests}, 200
        return {'message': 'Access Denied'}, 403


class ApproveRequest(Resource):
    """ Approve a request """
    @jwt_required
    def put(self, request_id):
        current_user = get_jwt_identity()
        if current_user['is_admin']:
            new_req = RequestModel()
            req = new_req.fetch_by_id(request_id)
            if not req:
                return {"message": f"request {request_id} doesn't exit."}, 404
            elif req["status"] != 'pending':
                return {'message': 'You can\'t approve this request, it\'s already been approved or rejected'}, 403
            new_req.approve(request_id)
            return {'message': 'Request Approved succcessfully'}, 200
        return {'message': 'Access Denied'}, 403


class RejectRequest(Resource):
    """ Reject a request """
    @jwt_required
    def put(self, request_id):
        current_user = get_jwt_identity()
        if current_user['is_admin']:
            new_req = RequestModel()
            req = new_req.fetch_by_id(request_id)
            if not req:
                return {"message": f"request {request_id} doesn't exit."}, 404
            elif req["status"] != 'pending':
                return {'message': 'You can\'t reject this request, it\'s already been approved or rejected'}, 403
            new_req.reject(request_id)
            return {'message': 'Request rejected succcessfully'}, 200
        return {'message': 'Access Denied'}, 403


class ResolveRequest(Resource):
    """ Resolve a request """

    @jwt_required
    def put(self, request_id):
        current_user = get_jwt_identity()
        if current_user['is_admin']:
            new_req = RequestModel()
            req = new_req.fetch_by_id(request_id)
            if not req:
                return {"message": f"request {request_id} doesn't exit."}, 404
            elif req["status"] != 'approve':
                return {'message': 'You can\'t resolve this request, it\'s either rejected or not approved'}, 403
            new_req.resolve(request_id)
            return {'message': 'Request resolved succcessfully'}, 200
        return {'message': 'Access Denied'}, 403


class UserRegistration(Resource):
    """ User Registration Resource """
    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True, type=str,
                        help="Name is required can only be a string")
    parser.add_argument('username', required=True, type=str,
                        help="Username is required and can only be a string")
    parser.add_argument('email', required=True, type=str,
                        help="Email is required")
    parser.add_argument('password', required=True,
                        help="Password is required")
    parser.add_argument('confirm_password', required=True,
                        help="Password confirmation is required")

    def post(self):
        """ Create a new User """
        args = UserRegistration.parser.parse_args()
        username = args.get("username").lower()

        if validate_username(username, 'Username'):
            return validate_username(username, 'Username')
        if validate_str_field(args["name"], 'Name'):
            return validate_str_field(args["name"], 'Name')
        if not re.match(r'(?=.*?[0-9])(?=.*?[A-Z])(?=.*?[a-z]).{6}', args['password']):
            return {"message": " Password rule: 1 digit, 1 caps, 1 number and minimum of 6 chars"}, 400
        if not re.match('[^@]+@[^@]+\.[^@]+', args['email']):
            return {"message": "Provide a valid email"}, 400

        user = User(username=username, name=args.get("name"),
                    email=args.get("email"), password=args.get("password"))
        username_taken = user.fetch_by_username(username)
        email_taken = user.fetch_by_email(args["email"])

        if username_taken:
            return {"message": "username already taken"}, 400
        elif email_taken:
            return {"message": "email already taken"}, 400
        elif args["password"] != args["confirm_password"]:
            return {
                "message": "password and confirm_password fields do not match"
            }, 400

        user.add()
        return {"message": "Account created successfully"}, 201


class UserSignin(Resource):
    """ User Signin Resource """
    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True, help="Username is required")
    parser.add_argument('password', required=True, help="Password is required")

    def post(self):
        """ Signin an existing User """
        args = UserSignin.parser.parse_args()
        username = args["username"].lower()
        password = args["password"]

        if validate_str_field(args["username"], 'Username'):
            return validate_str_field(args["username"], 'Username')

        new_user = User()
        user = new_user.fetch_by_username(username)

        if not user:
            return {"message": f"{username} does not have an account."}, 404
        if not new_user.check_password_hash(username, password):
            return {"message": "username or password do not match."}, 403
        access_token = create_access_token(identity=user)
        return {"access_token": access_token}, 200


api.add_resource(RequestList, '/api/v2/users/requests/')
api.add_resource(Request, '/api/v2/users/request/<string:request_id>/')
api.add_resource(AdminRequests, '/api/v2/requests/')
api.add_resource(
    ApproveRequest, '/api/v2/requests/<string:request_id>/approve/')
api.add_resource(
    RejectRequest, '/api/v2/requests/<string:request_id>/reject/')
api.add_resource(
    ResolveRequest, '/api/v2/requests/<string:request_id>/resolve/')
api.add_resource(UserRegistration, '/api/v2/users/auth/signup/')
api.add_resource(UserSignin, '/api/v2/users/auth/signin/')
# api.add_resource(UserSignout, '/api/v2/users/auth/signout/')
