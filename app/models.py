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
