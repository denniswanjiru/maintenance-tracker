import psycopg2
import os


def Store():
    def __init__(self):
        self.db_host = os.getenv('DB_HOST')
        self.db_name = os.getenv('DB_NAME')
        self.db_username = os.getenv('DB_USERNAME')
        self.db_password = os.getenv('DB_PASSWORD')
        self.conn = psycopg2.connect(
            database=self.db_name, host=self.db_host, user=self.db_username, password=self.db_password)
