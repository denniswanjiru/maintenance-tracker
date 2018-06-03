class Store():
    users = []
    requests = []

    @classmethod
    def add_user(cls, user):
        cls.users.append(user)

    @classmethod
    def add_request(cls, request):
        cls.requests.append(request)

    @classmethod
    def get_user_by_username(cls, username):
        for user in cls.users:
            if user.username == username:
                return user
        return None

    @classmethod
    def get_user_by_email(cls, email):
        for user in cls.users:
            if user.email == email:
                return user
        return None

    @classmethod
    def get_user_requests(cls, user_id):
        if cls.requests:
            my_requests = [
                _request for _request in cls.requests
                if _request.user_id == user_id]
            return my_requests
        return None


class User():
    def __init__(self, username, email, name, password):
        self.id = id(self)
        self.username = username
        self.email = email
        self.name = name
        self.password = password

    def check_password(self, password):
        if password == self.password:
            return True
        return False

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "name": self.name,
            "password": self.password
        }


class Request():
    def __init__(self, user_id, title, location, request_type, description):
        self.id = id(self)
        self.user_id = user_id
        self.title = title
        self.location = location
        self.request_type = request_type
        self.description = description

    def request_to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "location": self.location,
            "request_type": self.request_type,
            "description": self.description
        }
