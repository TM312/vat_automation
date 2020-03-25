# following http://www.patricksoftwareblog.com/structuring-a-flask-project/
import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, jsonify
from app.extensions import db, migrate, bcrypt, cors, mail

def create_app(env):
    from app.config import app_config
    app = Flask(__name__)
    app.config.from_object(app_config[env])
    register_extensions(app)
    register_api(app)

    # for testing purposes of the client (--> '.__init___test.py')
    @app.route("/ping")
    def ping():
        return jsonify("pong")

    return app


def register_extensions(app):
    # Since the application instance is now created, pass it to each Flask
    # extension instance to bind it to the Flask application instance (app)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    cors.init_app(app)
    mail.init_app(app)
    return None


def register_api(app):
    from flask_restx import Api
    from app.routes import register_routes
    api = Api(app, title="NT API", version="0.1.2")
    register_routes(api, app, root=os.getenv('API_ROOT'))
    return None
