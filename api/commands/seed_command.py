from datetime import datetime
from flask_script import Command

from app.extensions import db
from app.user import User


def seed_things():
    classes = [User]
    for klass in classes:
        seed_thing(klass)


def seed_thing(cls):
    things = [
        {
            'email': 'thomas.moellers@unisg.ch',
            'role': 'admin',
            'password': 'password1'
        },
        {
            'email': 'nico@gmail.com',
            'password': 'password2'
        },
        {
            'email': 'thomas@gmail.com',
            'password': 'password3'
        }
    ]
    db.session.bulk_insert_mappings(cls, things)


class SeedCommand(Command):
    """ Seed the DB."""

    def run(self):
        if (
            input(
                "Are you sure you want to drop all tables and recreate? (y/N)\n"
            ).lower()
            == "y"
        ):
            print("Dropping tables...")
            db.drop_all()
            db.create_all()
            seed_things()
            db.session.commit()
            print("DB successfully seeded.")
