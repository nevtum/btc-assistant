from application import configure_app
from config import FlaskConfig
from flask import Flask


def create_app(namespace):
    app = Flask(namespace)
    app.config.from_object(FlaskConfig)

    configure_app(app)
    return app

app = create_app(__name__)

if __name__ == '__main__':
    app.run()
