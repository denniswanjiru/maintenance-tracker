from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import uuid
import jwt
import os

from flask import current_app


class Store():
    """Store Model """

    def __init__(self):
        self.db_name = current_app.config['DB_NAME']
        self.db_host = current_app.config['DB_HOST']
        self.db_username = current_app.config['DB_USERNAME']
        self.db_password = current_app.config['DB_PASSWORD']
        self.conn = psycopg2.connect(
            database=self.db_name,
            host=self.db_host,
            user=self.db_username,
            password=self.db_password)
        self.cur = self.conn.cursor()

    def create_table(self, schema):
        self.cur.execute(schema)
        self.save()

    def drop_table(self, name):
        self.cur.execute('DROP TABLE IF EXISTS ' + name)
        self.save()

    def save(self):
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()


class User(Store):
    """ User Model """

    def __init__(
            self, username=None, name=None, email=None, password=None,
            is_admin=False):
        super().__init__()
        self.username = username
        self.name = name
        self.email = email
        self.is_admin = is_admin
        self.password_hash = "" if not password else generate_password_hash(
            password)

    def create(self):
        self.create_table(
            """
            CREATE TABLE users(
                id serial PRIMARY KEY,
                username VARCHAR NOT NULL UNIQUE,
                name VARCHAR NOT NULL,
                email VARCHAR NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                is_admin BOOLEAN NOT NULL
            );
            """
        )

    def drop(self):
        self.drop_table("users")

    def add(self):
        self.cur.execute(
            """
            INSERT INTO users (username, name, email, password_hash, is_admin)
            VALUES (%s , %s, %s, %s, %s)
            """,
            (self.username, self.name, self.email, self.password_hash, self.is_admin))

        self.save()

    def fetch_all(self):
        self.cur.execute("SELECT * FROM users")
        users_tuple = self.cur.fetchall()

        if users_tuple:
            return [self.serializer(user) for user in users_tuple]
        return None

    def fetch_by_username(self, username):
        self.cur.execute(
            "SELECT * FROM users where username=%s", (username, ))

        user = self.cur.fetchone()

        if user:
            return self.serializer(user)
        return None

    def fetch_by_email(self, email):
        self.cur.execute(
            "SELECT * FROM users where email=%s", (email, ))

        user = self.cur.fetchone()

        if user:
            return self.serializer(user)
        return None

    def check_password_hash(self, username, password):
        user = self.fetch_by_username(username)
        return check_password_hash(user["password_hash"], password)

    def serializer(self, user):
        return dict(
            id=user[0],
            username=user[1],
            name=user[2],
            email=user[3],
            password_hash=user[4],
            is_admin=user[5]
        )


class Request(Store):
    """ Request Model """

    def __init__(
            self, user_id=None, title=None, location=None, request_type=None,
            description=None, id=None, status="pending"):
        super().__init__()
        self.id = id
        self.user_id = user_id
        self.public_id = str(uuid.uuid4())
        self.title = title
        self.request_type = request_type
        self.location = location
        self.description = description,
        self.status = status

    def create(self):
        self.create_table(
            """
            CREATE TABLE requests(
                id serial PRIMARY KEY,
                public_id varchar NOT NULL UNIQUE,
                title varchar NOT NULL,
                location varchar NOT NULL,
                description text,
                user_id integer NOT NULL,
                request_type varchar NOT NULL,
                status varchar NOT NULL)
            """
        )

    def drop(self):
        self.drop_table("requests")

    def add(self):
        self.cur.execute(
            """
            INSERT INTO requests(
                public_id, title, location, description, user_id, request_type, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                self.public_id, self.title,
                self.location, self.description,
                self.user_id, self.request_type, self.status
            ))
        self.save()

    def fetch_all(self):
        self.cur.execute("SELECT * FROM requests")
        requests_tuple = self.cur.fetchall()
        requests = [self.serializer(request) for request in requests_tuple]
        return requests

    def fetch_by_id(self, public_id):
        self.cur.execute(
            "SELECT * FROM requests WHERE public_id=%s", (public_id, ))
        request_tuple = self.cur.fetchone()
        if request_tuple:
            return self.serializer(request_tuple)
        return None

    def fetch_by_user(self, user_id):
        """ Get users requests """
        self.cur.execute(
            "SELECT * FROM requests WHERE user_id=%s", (user_id, ))
        requests_tuple = self.cur.fetchall()
        if requests_tuple:
            return [self.serializer(request) for request in requests_tuple]
        return None

    def update(self, public_id):
        self.cur.execute(
            """
            UPDATE requests
            SET
            title = (%s),
            location = (%s),
            description = (%s),
            request_type = (%s)
            WHERE public_id = (%s)
             """,
            (self.title, self.location, self.description,
             self.request_type, public_id)
        )
        self.save()

    def approve(self, public_id):
        self.cur.execute(
            """
            UPDATE requests
            SET
            status = (%s)
            WHERE public_id = (%s)
             """,
            ('approved', public_id)
        )
        self.save()

    def reject(self, public_id):
        self.cur.execute(
            """
            UPDATE requests
            SET
            status = (%s)
            WHERE public_id = (%s)
             """,
            ('rejected', public_id)
        )
        self.save()

    def resolve(self, public_id):
        self.cur.execute(
            """
            UPDATE requests
            SET
            status = (%s)
            WHERE public_id = (%s)
             """,
            ('resolved', public_id)
        )
        self.save()

    def delete(self, public_id):
        self.cur.execute(
            "DELETE FROM requests WHERE public_id=%s", (public_id, ))
        self.save()

    def serializer(self, request):
        return dict(
            id=request[0],
            public_id=request[1],
            title=request[2],
            location=request[3],
            description=request[4],
            user_id=request[5],
            request_type=request[6],
            status=request[7]
        )
