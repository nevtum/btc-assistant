from application import configure_app
from flask import Flask

def create_app(namespace):
    app = Flask(namespace)

    configure_app(app)
    return app

app = create_app(__name__)

if __name__ == '__main__':
    app.run(debug=True)