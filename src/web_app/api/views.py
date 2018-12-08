from flask_restplus import Resource
from . import ns

@ns.route('/data')
class MyResource(Resource):
    def get(self):
        return {"hello": "world!"}, 200