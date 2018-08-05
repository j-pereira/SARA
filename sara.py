from datasetService import DatasetService
from associationRulesService import AssociationRulesService

print("\nSARA - Software para Análise de Regiões Ativas\n")

datasetService = DatasetService()
datasetService.setLastDateInDataset()

if datasetService.isDatasetUpdated() : 
    print("Already updated")
else :
    #datasetService.updateDataset()

    print("\n Association Rules ---- \n")

    associationRulesService = AssociationRulesService()
    associationRulesService.categorizeDataset()
    associationRulesService.createTransactionalDataset()


'''         
print("\n Association Rules ---- \n")

associationRulesService = AssociationRulesService()
associationRulesService.generateAssociationRules()


'''