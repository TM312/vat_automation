from faker import Faker
from sqlalchemy.exc import IntegrityError
from flask_script import Command

from app.extensions import db
from app.user import User

def create_users(count):
    fake = Faker()
    i = 0
    while i < count:
        u = User(
            email=fake.email(),
            password='1234'
        )
        db.session.add(u)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()

class FakeUserCreationCommand(Command):
    """ Seed the DB with Fake Users."""
    def run(self):
        if (input("Are you sure you want to drop all tables and create fake profiles? (y/N)\n").lower()== "y"):
            print("Dropping tables...")
            db.drop_all()
            db.create_all()
            create_users(count=4)
            print("DB seeded with fake users.")
