import os

from spleeterweb.app import create_app

FLASK_ENV = os.environ.get("FLASK_ENV", "development")
FLASK_DEBUG = os.environ.get("FLASK_DEBUG", True)

application = create_app()

if __name__ == "__main__":
    application.config["ENV"] = FLASK_ENV
    application.config["DEBUG"] = FLASK_DEBUG
    application.run()
