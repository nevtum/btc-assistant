from config import FlaskConfig
from flask import Flask
from presentation import configure_api, configure_app


def create_app(namespace):
    app = Flask(namespace)
    app.config.from_object(FlaskConfig)

    configure_app(app)
    configure_api(app)
    return app

app = create_app(__name__)

if __name__ == '__main__':
    app.run()
