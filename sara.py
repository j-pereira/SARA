from datasetService import DatasetService

print("\nSARA - Software para Análise de Regiões Ativas\n")

datasetService = DatasetService()
datasetService.setLastDateInDataset()

if datasetService.isDatasetUpdated() : 
    print("Already updated")
else :
    datasetService.updateDataset()