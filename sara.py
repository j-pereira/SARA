from srs import SRS
from sgas import SGAS
from datasetService import DatasetService



srs = SRS()
#srs.download(urlSRS)
#srs.readFile(srs.openFile())
#srs.fileLinesLen()
#srs.loadRegions()
#srs.printRegions()

print("\n ---- \n")

sgas = SGAS()
#sgas.download(urlSGAS)
#sgas.readFile(sgas.openFile())
#sgas.fileLinesLen()
#sgas.setHeadersColumnPosition(sgas.loadFilesHeader())
#sgas.loadEvents()
#sgas.printEvents()

print("\n ---- \n")

datasetService = DatasetService()
datasetService.setLastDateInDataset()

if datasetService.isDatasetUpdated() : 
    print("Already updated")
else :
    datasetService.setListOfDaysToUpdate()
datasetService.printListOfDaysToUpdate()

datasetService.verifyYearsNeedingUpdate()
datasetService.printYearsToUpdate()
datasetService.downloadRegionFiles()