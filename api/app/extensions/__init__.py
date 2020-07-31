from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
cors = CORS(supports_credentials=True, resources={r"/*": {"origins": "*"}})
mail = Mail()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["10 per minute", "5 per second"]
    )
