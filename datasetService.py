import urllib.request
from datetime import datetime, timedelta
from srs import SRS
from sgas import SGAS

class DatasetService :
    lastDateInDataset = datetime.today().date()
    today = datetime.today().date()
    fileLines = list()
    listOfDaysToUpdate = list()
    



    def setLastDateInDataset(self) :         
        _file = open("files/dataset.txt")
        
        for line in _file :
            self.fileLines.append(line)

        l = self.fileLines[-1].split(",")
        strDate = l[0] + l[1] + l[2]
        date = datetime.strptime(strDate, "%Y%b%d").date()
        print(date)
        self.lastDateInDataset = datetime.strptime(strDate, "%Y%b%d").date()
        
    
    def isDatasetUpdated(self) : 
        if self.lastDateInDataset == self.today :
            return True
        else :
            return False
    
    
    def setListOfDaysToUpdate(self) : 
        print(self.lastDateInDataset)
        print(self.today)

        d = self.lastDateInDataset
        delta = timedelta(1)
        while d <= self.today:
            self.listOfDaysToUpdate.append(d.strftime("%Y-%m-%d"))
            d += delta


        print("COMEÇA AQUIIII      ------ ")

        for date in self.listOfDaysToUpdate :
            print(date)






'''

    def updateDataset(self, lastDateInDataset) : 

    def saveDatasetInCSVFile(self) : 

    def loadRegionFiles(self) : 
    
    def loadEventsFiles(self) : 

    def matchRegionsEvents(self) : 

'''