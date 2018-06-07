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
        self.id = id
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
