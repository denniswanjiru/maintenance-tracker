from app import app
from db import init, drop
from app.models import User


@app.cli.command()
def init_db():
    """ Creates tables """
    init()


@app.cli.command()
def drop_db():
    """ Drops tables """
    drop()


@app.cli.command()
def create_admin():
    """ Creates a Super Admin """
    admin = User(username="admin", name="Super Admin",
                 password="secret", email="admin@app.com", is_admin=True)
    admin.add()
