from app.models import User, Request


def init():
    user = User()
    request = Request()

    user.create()
    request.create()


def drop():
    user = User()
    request = Request()

    user.drop()
    request.drop()
