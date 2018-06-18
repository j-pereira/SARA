from datasetService import DatasetService

print("\nSARA - Software para Análise de Regiões Ativas\n")

datasetService = DatasetService()
datasetService.setLastDateInDataset()

if datasetService.isDatasetUpdated() : 
    print("Already updated")
else :
    datasetService.setListOfDaysToUpdate()
    #datasetService.printListOfDaysToUpdate()
    datasetService.verifyYearsNeedingUpdate()
    #datasetService.printYearsToUpdate()
    #datasetService.downloadFiles()

    print("\n ---- \n")

    datasetService.loadRegionsToUpdate()
    datasetService.printRegionsToUpdate()

    print("\n ---- \n")

    datasetService.loadEventsToUpdate()
    datasetService.printEventsToUpdate()
    print("\n ---- \n")

    datasetService.printListMagConfiguration(datasetService.createDatasetFileLines())