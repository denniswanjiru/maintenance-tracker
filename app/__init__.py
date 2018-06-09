from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from functools import wraps
from flask_jwt_extended import (
    jwt_required, JWTManager, create_access_token, get_jwt_identity
)
from .models import User, Request as RequestModel
import os

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET')
jwt = JWTManager(app)
jwt.unauthorized_loader(app)
api = Api(app)
CORS(app)


def find_request(request_id, user_id):
    """ Find a specific request resource based off the id and users' id """
    return [
        _request if _request['request_id'] == request_id and
        _request["user_id"] == user_id else "does_not_belong_to"
        for _request in requests_store
        if _request['request_id'] == request_id
    ]


class RequestList(Resource):
    """ Resource for list request """

    parser = reqparse.RequestParser()
    parser.add_argument('title', required=True, type=str)
    parser.add_argument('location', required=True, type=str)
    parser.add_argument('request_type', required=True)
    parser.add_argument('description')

    @jwt_required
    def get(self):
        """ Get all request """
        user_id = get_jwt_identity()
        # print(user_id)
        request = RequestModel()

        my_requests = request.fetch_by_user(user_id)

        if my_requests:
            return {"requests": my_requests}, 200
        return {"message": "You don't have any requests yet"}, 404

    @jwt_required
    def post(self):
        """ Create a new request """
        user_id = get_jwt_identity()
        args = RequestList.parser.parse_args()

        _request = RequestModel(
            user_id=user_id, title=args['title'], location=args['location'],
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
        user_id = get_jwt_identity()
        req = RequestModel()
        _request = req.fetch_by_id(request_id)

        if not _request:
            return {"message": f"request {request_id} doesn't exit."}, 404
        elif _request["user_id"] != user_id:
            return {"message": "You can only view your own requests"}, 403
        return {'request': _request}, 200

    @jwt_required
    def delete(self, request_id):
        """ Delete a single request resource based off its id """
        user_id = get_jwt_identity()
        req = RequestModel()
        _request = req.fetch_by_id(request_id)

        if not _request:
            return {"message": f"request {request_id} doesn't exit."}, 404
        elif _request["user_id"] != user_id:
            return {"message": "You can only delete your own requests"}, 403
        req.delete(_request["public_id"])
        return {"message": "Your request was successfully deleted"}, 200


class UserRegistration(Resource):
    """ User Registration Resource """
    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True, type=str)
    parser.add_argument('username', required=True, type=str)
    parser.add_argument('email', required=True, type=str)
    parser.add_argument('password', required=True)
    parser.add_argument('confirm_password', required=True)

    def post(self):
        """ Create a new User """
        args = UserRegistration.parser.parse_args()

        user = User(username=args.get("username"), name=args.get("name"),
                    email=args.get("email"), password=args.get("password"))

        username_taken = user.fetch_by_username(args["username"])
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
        username = args["username"]
        password = args["password"]

        user = User()
        user = user.fetch_by_username(username)

        if not user:
            return {"message": f"{username} does not have an account."}, 404
        if user['password'] != password:
            return {"message": "username or password do not match."}, 403
        access_token = create_access_token(identity=user["id"])
        return {"access_token": access_token}, 200


api.add_resource(RequestList, '/api/v1/users/requests/')
api.add_resource(Request, '/api/v1/users/request/<string:request_id>/')
api.add_resource(UserRegistration, '/api/v1/users/auth/signup/')
api.add_resource(UserSignin, '/api/v1/users/auth/signin/')
# api.add_resource(UserSignout, '/api/v1/users/auth/signout/')
