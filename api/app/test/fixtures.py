from dotenv import load_dotenv
load_dotenv()

import pytest

from app import create_app


@pytest.fixture
def app():
    return create_app("test")


@pytest.fixture
def client(app):
    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    return app.test_client()


@pytest.fixture
def db(app):
    from app.extensions import db
    # setting up the application context
    # read here: https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/

    with app.app_context():  # 'with' takes care of setup and teardown (instead of 'app.app_context().push()' )

        #making sure db is empty
        db.drop_all()
        db.create_all()

        yield db  # this is where the testing happens!

        db.session.commit()
        db.drop_all()
        db.session.commit()
