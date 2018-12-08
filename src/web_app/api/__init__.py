from flask import Blueprint
from flask_restplus import Api, Namespace

bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(bp, version='0.1', title='Bitcoin analysis API')

ns = Namespace('market', description='Price related operations')
api.add_namespace(ns)

from . import views

def configure_api(app):
    app.register_blueprint(bp)
