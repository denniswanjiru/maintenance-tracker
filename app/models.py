import psycopg2
import os


class Store():
    def __init__(self):
        self.db_host = os.getenv('DB_HOST')
        self.db_name = os.getenv('DB_NAME')
        self.db_username = os.getenv('DB_USERNAME')
        self.db_password = os.getenv('DB_PASSWORD')
        self.conn = psycopg2.connect(
            database=self.db_name, host=self.db_host, user=self.db_username, password=self.db_password)
        self.cur = self.conn.cursor()

    def create_table(self, schema):
        self.cur.execute(schema)
        self.save()

    def save(self):
        self.conn.commit()


class User(Store):
    def __init__(self, username, name, email, password):
        super().__init__()
        self.username = username
        self.name = name
        self.email = email
        self.password_hash = password

    def create(self):
        self.create_table(
            """
            CREATE TABLE users(
                id serial PRIMARY KEY,
                username varchar NOT NULL UNIQUE,
                name varchar NOT NULL,
                email varchar NOT NULL UNIQUE,
                password_hash text NOT NULL
            );
            """
        )

    def add(self):
        self.cur.execute(
            """
            INSERT INTO users (username, name, email, password_hash)
            VALUES (%s , %s, %s, %s)
            """,
            (self.username, self.name, self.email, self.password_hash))

        self.save()

    def fetch_all(self):
        self.cur.execute("SELECT * FROM users")
        users_tuple = self.cur.fetchall()
        users = []

        if user:
            for user in users_tuple:
                users.append(self.serializer(user))

            print(users)
        return None

    def fetch_by_username(self, username):
        self.cur.execute(
            "SELECT * FROM users where username=%s", (username, ))

        user = self.cur.fetchone()

        if user:
            return self.serializer(user)
        return None

    def serializer(self, user):
        return dict(
            id=user[0],
            username=user[1],
            name=user[2],
            email=user[3],
            password=user[4]
        )


class Request(Store):
    def __init__(self, user_id, title, request_type, location, description):
        super().__init__()
        self.id = id
        self.user_id = user_id
        self.title = title
        self.request_type = request_type
        self.location = location
        self.description = description

    def create(self):
        self.create_table(
            """
            CREATE TABLE requests(
                id serial PRIMARY KEY,
                uuid varchar NOT NULL UNIQUE,
                title varchar NOT NULL,
                location varchar NOT NULL,
                description text,
                user_id  SERIAL REFERENCES users,
                request_type varchar NOT NULL)
            """
        )
