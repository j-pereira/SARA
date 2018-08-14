from flask import Flask
from flask_restful import Resource, Api
from saraController import AssociationRules

app = Flask(__name__)
api = Api(app)

api.add_resource(AssociationRules, '/')

if __name__ == '__main__':
    app.run(debug=True)





'''
print("\nSARA - Software para Análise de Regiões Ativas\n")

datasetService = DatasetService()
datasetService.setLastDateInDataset()

if datasetService.isDatasetUpdated() : 
    print("Already updated")
else :
    datasetService.updateDataset()

    print("\n Association Rules ---- \n")

    associationRulesService = AssociationRulesService()
    associationRulesService.categorizeDataset()
    associationRulesService.createTransactionalDataset()
    associationRulesService.generateAssociationRules()
'''

