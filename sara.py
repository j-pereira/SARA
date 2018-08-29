from flask import Flask
from flask_restful import Resource, Api
from saraController import AssociationRulesController
from saraController import DatasetController

app = Flask(__name__)
api = Api(app)

api.add_resource(AssociationRulesController, '/associationrules')
api.add_resource(DatasetController, '/dataset')

if __name__ == '__main__':
    app.run(debug=True)

