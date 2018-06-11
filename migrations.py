from app.models import Store, User, Request


def init():
    user = User()
    request = Request()

    user.create()
    request.create()


init()