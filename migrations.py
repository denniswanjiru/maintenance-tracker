from cls import Store

db = Store()


def up():
    db.create_table(
        '''
        CREATE TABLE users(
        id serial PRIMARY KEY,
        username varchar NOT NULL UNIQUE,
        name varchar NOT NULL ,
        email varchar NOT NULL UNIQUE,
        password_hash text NOT NULL)
        '''
    )

    db.create_table(
        '''
        CREATE TABLE requests(
        id serial PRIMARY KEY,
        uuid varchar NOT NULL UNIQUE,
        title varchar NOT NULL,
        location varchar NOT NULL,
        description text,
        user_id  SERIAL REFERENCES users,
        request_type varchar NOT NULL)
        '''
    )


def down(*args):
    for arg in args:
        db.drop_table(arg)
