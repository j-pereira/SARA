import urllib.request
from datetime import datetime, timedelta
import os
import shutil
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
    regionsToUpdate = list()
    eventsToUpdate = list()
        



    def setLastDateInDataset(self) :         
        _file = open("files/dataset.txt")
        for line in _file :
            self.fileLines.append(line)

        l = self.fileLines[-1].split(",")
        strDate = l[0] + l[1] + l[2]
        date = datetime.strptime(strDate, "%Y%b%d").date()
        self.lastDateInDataset = datetime.strptime(strDate, "%Y%b%d").date()
        print("Last day in dataset: " + str(self.lastDateInDataset))
        
    
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


    def downloadFiles(self) : 
        DatasetService.createFolders(self.yearsToUpdate, "SRS")
        DatasetService.createFolders(self.yearsToUpdate, "SGAS")
        lastYear = self.yearsToUpdate[-1]

        for year in self.yearsToUpdate : 
            print(year + " - " + lastYear)

            if year == lastYear : 
                daysOfLastYear = DatasetService.daysOfLastYear(self.listOfDaysToUpdate, lastYear)
                for date in daysOfLastYear : 
                    self.srs.downloadDay(self.url, date[:4], date)
                    self.sgas.downloadDay(self.url, date[:4], date)
            else :
                self.srs.downloadHoleYear(self.url, year)
                DatasetService.organizeFiles(self.srs.filePath, year, "SRS", self.srs.tarFileName)

                self.sgas.downloadHoleYear(self.url, year)
                DatasetService.organizeFiles(self.sgas.filePath, year, "SGAS", self.sgas.tarFileName)



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
    def organizeFiles(filePath, year, _type, tarFileName) : 
        DatasetService.unzipfile(filePath + year + "/" + year + tarFileName, filePath + year + "/")
        DatasetService.deleteFile(filePath + year + "/" + year + tarFileName)
        DatasetService.moveFiles(filePath, year, _type)



    @staticmethod
    def unzipfile(zipFile, targetPath) : 
        tar = tarfile.open(zipFile, "r:gz")
        tar.extractall(targetPath)
        tar.close()


    @staticmethod
    def deleteFile(path) : 
        os.remove(path)


    @staticmethod
    def moveFiles(filePath, year, _type) : 
        path = filePath + year + "/" + _type + "/"
        newpath = filePath + year + "/"
        for filename in os.listdir(path) : 
            if not os.path.exists(newpath + filename) : 
                os.rename(path + filename, newpath + filename)
        shutil.rmtree(path)

    
    
    
    def loadRegionsToUpdate(self) : 
        for day in self.listOfDaysToUpdate : 
            self.srs.readFile(self.srs.openFile(day[:4], day))
            self.srs.loadRegions()
            if self.srs.regions : 
                self.regionsToUpdate.extend(self.srs.regions)
            self.srs.clearLists()
        

    def loadEventsToUpdate(self) : 
        for day in self.listOfDaysToUpdate : 
            self.sgas.readFile(self.sgas.openFile(day[:4], day))
            self.sgas.setHeadersColumnPosition(self.sgas.loadFilesHeader())
            self.sgas.loadEvents()
            if self.sgas.events : 
                self.eventsToUpdate.extend(self.sgas.events)
            self.sgas.clearLists()
        
    
    def printRegionsToUpdate(self) : 
        print("PRINT REGIONS TO UPDATE: ")
        for region in self.regionsToUpdate : 
            print(region.year + " | " + region.month + " | " + region.day  + " | " + region.id  + " | " + region.area  + " | " + region.sunspotNmbr  + " | " + region.sunspotClassification)



    def printEventsToUpdate(self) : 
        print("\nPRINT EVENTS TO UPDATE: ")
        for event in self.eventsToUpdate : 
            print(event.year + " | " + event.month + " | " + event.day + " | " + event.region + " | " + event.xRay + " | " + event.cmRadio)
        



    def createDatasetFileLines(self) : 
        listMagConfiguration = list()
        magConfiguration = ["", "", "", "", "", "", "", "", ""]
        for region in self.regionsToUpdate : 
            magConfiguration[0] = region.year
            magConfiguration[1] = region.month
            magConfiguration[2] = region.day
            magConfiguration[3] = region.id
            magConfiguration[4] = region.area
            magConfiguration[5] = region.sunspotNmbr
            magConfiguration[6] = region.sunspotClassification

            flag = False
            for event in self.eventsToUpdate : 
                if (region.year == event.year) and (region.month == event.month) and (region.day == event.day) and (region.id == event.region) : 
                    magConfiguration[7] = event.xRay
                    magConfiguration[8] = event.cmRadio

                    flag = True
                    line = magConfiguration[0] + "," + magConfiguration[1] + "," + magConfiguration[2] + "," + magConfiguration[3] + "," + magConfiguration[4] + "," + magConfiguration[5] + "," + magConfiguration[6]  + "," + magConfiguration[7] + "," + magConfiguration[8]
                    listMagConfiguration.append(line)
            
            if flag == False : 
                line = magConfiguration[0] + "," + magConfiguration[1] + "," + magConfiguration[2] + "," + magConfiguration[3] + "," + magConfiguration[4] + "," + magConfiguration[5] + "," + magConfiguration[6]  + "," + magConfiguration[7] + "," + magConfiguration[8]
                listMagConfiguration.append(line)
            
            for i in range(len(magConfiguration)) : 
                magConfiguration[i] = ""
            
        return listMagConfiguration
    





    def printListMagConfiguration(self, listMagConfiguration) : 
        print("\n\nPRINT LIST MAGCONFIG: ")
        for m in listMagConfiguration : 
            print(m)




            


                    











    #def updateDataset(self) : 
        




'''



    def updateDataset(self, lastDateInDataset) : 

    def saveDatasetInCSVFile(self) : 

    def loadRegionFiles(self) : 
    
    def loadEventsFiles(self) : 

    def matchRegionsEvents(self) : 

'''