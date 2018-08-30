from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from saraController import AssociationRulesController
from saraController import DatasetController

app = Flask(__name__)
api = Api(app)
CORS(app, resources={r"/*": {"origins": "*"}})

api.add_resource(AssociationRulesController, '/associationrules')
api.add_resource(DatasetController, '/dataset')

if __name__ == '__main__':
    app.run(debug=True)

