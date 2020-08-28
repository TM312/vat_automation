import os
from dotenv import load_dotenv
load_dotenv()

from app import create_app, create_celery

env = os.getenv("FLASK_ENV")
app = create_app(env)
celery = create_celery(app=app)

if __name__ == "__main__":
    from app.extensions import socket_io
    socket_io.run(app=app)
    #app.run()
