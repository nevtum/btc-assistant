from flask import Blueprint

bp = Blueprint("main", __name__, url_prefix="/")

from . import views

def configure_app(app):
    app.register_blueprint(bp)