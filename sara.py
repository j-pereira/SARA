from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from saraController import AssociationRulesController
from saraController import OriginalDataset
from saraController import ClassifiedDataset
from saraController import LastDateDataset
from saraController import UpdateDataset

app = Flask(__name__)
api = Api(app)
CORS(app, resources={r"/*": {"origins": "*"}})

api.add_resource(AssociationRulesController, '/associationrules')
api.add_resource(OriginalDataset, '/dataset/original')
api.add_resource(ClassifiedDataset, '/dataset/classified')
api.add_resource(LastDateDataset, '/dataset/lastdate')
api.add_resource(UpdateDataset, '/dataset/update')

if __name__ == '__main__':
    app.run(debug=True)

 