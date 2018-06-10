from app import app
from db import init, drop


@app.cli.command()
def init_db():
    ''' Create tables'''
    init()


@app.cli.command()
def drop_db():
    ''' Drop tables'''
    drop()
