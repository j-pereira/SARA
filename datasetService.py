import urllib.request
from datetime import datetime, timedelta
import os
import tarfile
from srs import SRS
from sgas import SGAS

class DatasetService :
    srs = SRS()
    sgas = SGAS()
    url = "ftp://ftp.swpc.noaa.gov/pub/warehouse/"
    lastDateInDataset = datetime.today().date()
    today = datetime.today().date()
    fileLines = list()
    listOfDaysToUpdate = list()
    yearsToUpdate = list()
    



    def setLastDateInDataset(self) :         
        _file = open("files/dataset.txt")
        
        for line in _file :
            self.fileLines.append(line)

        l = self.fileLines[-1].split(",")
        strDate = l[0] + l[1] + l[2]
        date = datetime.strptime(strDate, "%Y%b%d").date()
        self.lastDateInDataset = datetime.strptime(strDate, "%Y%b%d").date()
        
    
    def isDatasetUpdated(self) : 
        if self.lastDateInDataset == self.today :
            return True
        else :
            return False
    
    
    def setListOfDaysToUpdate(self) : 
        delta = timedelta(1)
        day = self.lastDateInDataset + delta
        while day <= self.today :
            self.listOfDaysToUpdate.append(day.strftime("%Y%m%d"))
            day += delta

    def printListOfDaysToUpdate(self) : 
        print("LIST OF DAYS TO UPDATE COMEÇA AQUIIII    ------ ")
        for date in self.listOfDaysToUpdate :
            print(date)

    def verifyYearsNeedingUpdate(self) : 
        year = ""
        for date in self.listOfDaysToUpdate : 
            if year != date[:4] :
                self.yearsToUpdate.append(date[:4])
            year = date[:4]
        self.yearsToUpdate
            
    def printYearsToUpdate(self) : 
        for year in self.yearsToUpdate :
            print(year)


    def downloadRegionFiles(self) : 
        DatasetService.createFolders(self.yearsToUpdate, "SRS")
        lastYear = self.yearsToUpdate[-1]

        for year in self.yearsToUpdate : 
            print(len(self.yearsToUpdate))
            print(year + " - " + lastYear)

            if year == lastYear : 
                daysOfLastYear = DatasetService.daysOfLastYear(self.listOfDaysToUpdate, lastYear)
                for date in daysOfLastYear : 
                    self.srs.downloadDay(self.url, date[:4], date)
            else :
                self.srs.downloadHoleYear(self.url, year)
                DatasetService.unzipfile("files/SRS/" + year + "/" + year + "_SRS.tar.gz", "files/SRS/" + year + "/")
            


    @staticmethod
    def daysOfLastYear(listOfDaysToUpdate, lastYear) : 
        daysOfLastYear = list()
        for date in listOfDaysToUpdate : 
            if date[:4] == lastYear :
                daysOfLastYear.append(date)
        return daysOfLastYear


    @staticmethod
    def createFolders(yearsToUpdate, _type) :
        for year in yearsToUpdate : 
            if not os.path.exists("files/" + _type + "/" + year):
                os.makedirs("files/" + _type + "/" + year)
    

    @staticmethod
    def unzipfile(zipFile, targetPath) : 
        tar = tarfile.open(zipFile, "r:gz")
        tar.extractall(targetPath)
        tar.close()




'''

    def updateDataset(self, lastDateInDataset) : 

    def saveDatasetInCSVFile(self) : 

    def loadRegionFiles(self) : 
    
    def loadEventsFiles(self) : 

    def matchRegionsEvents(self) : 

'''