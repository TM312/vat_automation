# following http://www.patricksoftwareblog.com/structuring-a-flask-project/
from app.extensions import db, migrate, bcrypt, mail, cors, limiter
#from app.logs.service import LogService
from flask import Flask, jsonify
from werkzeug.contrib.fixers import ProxyFix
from dotenv import load_dotenv
load_dotenv()


def create_app(env):
    from app.config import app_config
    app = Flask(__name__)
    app.config.from_object(app_config[env])
    # for example if the request goes through one proxy before hitting your application server
    app.wsgi_app = ProxyFix(app.wsgi_app, num_proxies=1)
    register_extensions(app)
    register_api(app)
    # !!! LogService.setup_logging(app)

    # for testing purposes of the client (--> '.__init__test.py')
    @app.route("/ping_3f5ca2711e72a507")
    def ping():
        return jsonify("pong_3f5ca2711e72a507")


    @app.teardown_request
    def teardown_request(exception):
        if exception:
            db.session.rollback()
        db.session.remove()
        print('RUN ON TEARDOWN', flush=True)

    return app


def register_extensions(app):
    # Since the application instance is now created, pass it to each Flask
    # extension instance to bind it to the Flask application instance (app)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    cors.init_app(app)
    mail.init_app(app)
    limiter.init_app(app)

    return None


def register_api(app):
    from flask_restx import Api
    from app.routes import register_routes
    api = Api(app, title="Tax-Automation API", version="0.1.0")
    register_routes(api, app)
    #register_routes(api, app, root=os.getenv('API_ROOT'))
    return None
