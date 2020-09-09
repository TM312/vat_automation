from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_caching import Cache
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_socketio import SocketIO

db = SQLAlchemy()
migrate = Migrate()
# ma = Marshmallow()
bcrypt = Bcrypt()
cors = CORS(supports_credentials=True, resources={r"/*": {"origins": "*"}}) #!!!! addd domain later
mail = Mail()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["10 per minute", "5 per second"]
)

session = Session()
cache = Cache()
socket_io = SocketIO(
    manage_session=False,
    cors_allowed_origins="*",  # !!!! addd domain later
    logger=True,
    engineio_logger=True)
