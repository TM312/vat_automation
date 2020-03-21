import os
from dotenv import load_dotenv
load_dotenv()

from app import create_app

env = os.getenv("FLASK_ENV")
app = create_app(env)

if __name__ == "__main__":
    app.run()
