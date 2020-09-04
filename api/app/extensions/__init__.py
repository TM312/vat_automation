from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_caching import Cache
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from .socketio import socket_io

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
cors = CORS(supports_credentials=True, resources={r"/*": {"origins": "*"}}) #!!!! addd domain later
mail = Mail()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["10 per minute", "5 per second"]
)

session = Session()
cache = Cache()
