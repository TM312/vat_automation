from sqlalchemy.exc import IntegrityError
from flask_script import Command

from app.extensions import db
from app.namespaces.user import User


def create_initial_users():
    t = User(
        email='thomas.moellers@unisg.ch',
        role='admin',
        password='ad51bd4a1d59e9fe75f7a988dc6c1442',
        claimed=True,
        company_name='tax-automation.com'
    )
    db.session.add(t)

    # n = User(
    #     email='nico@gmail.com',
    #     password='1234'
    # )
    # db.session.add(n)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()


class InitialUserCreationCommand(Command):
    """ Seed the DB with Initial Users."""

    def run(self):
        print("Dropping tables...")
        db.drop_all()
        db.create_all()
        create_initial_users()
        print("DB seeded with the initial users.")
