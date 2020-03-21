import os
from flask_script import Manager
from flask_migrate import MigrateCommand

from app import create_app
from app.extensions import db

from commands.fake import FakeUserCreationCommand
from commands.initial import InitialUserCreationCommand

from dotenv import load_dotenv
load_dotenv()

env = os.getenv("FLASK_ENV")
print(f"Active environment: * {env} *")
app = create_app(env)

manager = Manager(app)
app.app_context().push()

manager.add_command("fake_users_db", FakeUserCreationCommand)
manager.add_command("initial_users_db", InitialUserCreationCommand)
manager.add_command('db', MigrateCommand)

@manager.command
def run():
    app.run()

@manager.command
def init_db():
    db.drop_all()
    print("Creating all resources.")
    db.create_all()

@manager.command
def drop_all():
    if input("Are you sure you want to drop all tables? (y/N)\n").lower() == "y":
        print("Dropping tables...")
        db.drop_all()


if __name__ == "__main__":
    manager.run()
