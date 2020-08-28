# following http://www.patricksoftwareblog.com/structuring-a-flask-project/
from app.extensions import (db, migrate, bcrypt, mail, cors, limiter, cache, session, socket_io)
#from app.logs.service import LogService
from flask import Flask, jsonify
from werkzeug.contrib.fixers import ProxyFix
from dynaconf.contrib import FlaskDynaconf
from celery import Celery
from dotenv import load_dotenv
load_dotenv()


def create_app(env):
    from app.config import app_config
    app = Flask(__name__)
    app.config.from_object(app_config[env])
    # for example if the request goes through one proxy before hitting your application server
    app.wsgi_app = ProxyFix(app.wsgi_app, num_proxies=1)

    # make app.config support dot notation.
    FlaskDynaconf(app=app)

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

    return app


def register_extensions(app) -> None:
    # Since the application instance is now created, pass it to each Flask
    # extension instance to bind it to the Flask application instance (app)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    cors.init_app(app)
    mail.init_app(app)
    limiter.init_app(app)
    session.init_app(app)

    # init Cache
    cache.init_app(app, {
        "CACHE_TYPE": "redis",
        "CACHE_REDIS_URL": app.config.CACHE_REDIS_URL
    })

    # init SocketIO
    if not app.config.CELERY_BROKER_URL:
        logging.warn(
            """app.config.CELERY_BROKER_URL is not set. """
            """SocketIO may not work with Celery workers now.""")

    socket_io.init_app(app=app, message_queue=app.config.CELERY_BROKER_URL)

    return None


def register_api(app):
    from flask_restx import Api
    from app.routes import register_routes
    api = Api(app, title="Tax-Automation API", version="0.1.0")
    register_routes(api, app)
    #register_routes(api, app, root=os.getenv('API_ROOT'))
    return None


def create_celery(app):
    """
    Initializes a celery application using Flask App
        (retrieved from `http://flask.pocoo.org/docs/1.0/patterns/celery/`).
    """
    celery = Celery(app.import_name,
                    broker=app.config.CELERY_BROKER_URL,
                    backend=app.config.CELERY_RESULT_BACKEND)
    # celery.conf.update(app.config)
    celery.conf.CELERY_IMPORTS = app.config.CELERY_IMPORTS
    celery.conf.BROKER_HEARTBEAT = app.config.CELERY_BROKER_HEARTBEAT

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
