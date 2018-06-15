import urllib.request
from region import Region

class SRS : 
    filePath = "files/SRS/"
    fileLines = list()
    regions = list()


    
    def downloadHoleYear(self, url, year) : 
        filesName = year + "_SRS.tar.gz"
        url = url + year + "/" + filesName
        path = self.filePath + year + "/" + filesName
        urllib.request.urlretrieve(url, path)

    
    def downloadDay(self, url, year, day) : 
        filesName = "/" + day + "SRS.txt" 
        url = url + year + "/SRS" + filesName
        path = self.filePath + year + filesName
        print(url)
        print(path)
        urllib.request.urlretrieve(url, path)


    def openFile(self) : 
        return open(self.filePath)

    def readFile(self, _file) :
        for line in _file:
            self.fileLines.append(line)
    
    def fileLinesLen(self) :
        print("Tamanho do arquivo: " + str(len(self.fileLines)))

    def printSomeLines(self) :
        for line in self.fileLines:
            if line[0] != "#" and line[0] != ":" :
                print(line)
    
    def loadRegions(self) : 
        flag = False
        year = ""
        month = ""
        day = ""

        for line in self.fileLines : 
            lineSplited = line.split(" ")
            
            if lineSplited[0] == ":Issued:" :
                year = lineSplited[1]
                month = lineSplited[2]
                day = lineSplited[3]

            if flag == True :
                if lineSplited[0] == "IA." :
                    break
                else :
                    if lineSplited[0] == "None\n" :
                        break
                    else :
                        region = Region()
                        region.year = year
                        region.month = month
                        region.day = day
                        region.id = lineSplited[0]
                        region.area = lineSplited[6]
                        region.sunspotNmbr = lineSplited[12]
                        region.sunspotClassification = lineSplited[13]
                        self.regions.append(region)
            
            if lineSplited[0] == "Nmbr" : 
                flag = True


    def printRegions(self) :
        print("PRINT REGIONS: ")
        for region in self.regions :
            print(region.year + " | " + region.month + " | " + region.day  + " | " + region.id  + " | " + region.area  + " | " + region.sunspotNmbr  + " | " + region.sunspotClassification)

    

