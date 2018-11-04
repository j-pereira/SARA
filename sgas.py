import urllib.request
from header import Header
from event import Event

class SGAS:
    filePath = "files/SGAS/"
    tarFileName = "_SGAS.tar.gz"
    dayFileName = "SGAS.txt"
    fileLines = list()
    events = list()


    
    def downloadHoleYear(self, url, year) : 
        filesName = year + self.tarFileName
        url = url + year + "/" + filesName
        path = self.filePath + year + "/" + filesName
        urllib.request.urlretrieve(url, path)
        print("Downloaded: " + url)

    
    def downloadDay(self, url, year, day) : 
        filesName = "/" + day + self.dayFileName 
        url = url + year + "/SGAS" + filesName
        path = self.filePath + year + filesName
        urllib.request.urlretrieve(url, path)
        print("Downloaded: " + url)
 
    
    def openFile(self, year, day) : 
        return open(self.filePath + year + "/" + day + self.dayFileName)


    def readFile(self, _file) :
        for line in _file:
            self.fileLines.append(line)
        _file.close()
    

    def fileLinesLen(self) :
        print("Tamanho do arquivo: " + str(len(self.fileLines)))


    def printSomeLines(self) :
        for line in self.fileLines:
            print(line.split(" "))
    

    def loadEvents(self) : 
        flag = False
        year = ""
        month = ""
        day = ""

        for line in self.fileLines : 
            lineSplited = line.split(" ")
            print(lineSplited)

            if lineSplited[0] == ":Issued:" :
                year = lineSplited[1]
                month = lineSplited[2]
                day = lineSplited[3]
                        
            if flag == True :
                if lineSplited[0] == "B." : 
                    break
                else : 
                    if line == "None\n" : 
                        break
                    else : 
                        
                        event = Event()
                        event.year = year
                        event.month = month
                        event.day = day
                        event.region = SGAS.findAttribute(line, "region")
                        event.xRay = SGAS.findAttribute(line, "xray")
                        event.cmRadio = SGAS.findAttribute(line, "radio")
                        if (event.region != "") and ((event.xRay != "") or (event.cmRadio != "")) : 
                            self.events.append(event)

            if lineSplited[0] == "Begin" : 
                flag = True

                

    @staticmethod
    def findAttribute(line, flag) : 
        attribute = ""
        cont = 0

        if flag == "region" :
            cont = Header.region
        elif flag == "xray" : 
            cont = Header.xRay
        elif flag == "radio" :
            cont = Header.cmRadio
        
        print(line)
        print(cont)

        while line[cont] != " " :
            cont = cont - 1

        pos = cont + 1
        while line[pos] != " " :
            attribute += line[pos]
            pos += 1
        
        return attribute


    

    def loadFilesHeader(self) :
        header = ""
        for line in self.fileLines : 
            lineSplited = line.split(" ")
            if lineSplited[0] == "Begin" : 
                header = line
                break
        return header
    

    def setHeadersColumnPosition(self, headersLine) : 
        for i in range(len(headersLine)) :
            if headersLine[i] != " " :
                char = headersLine[i]
                if char == "R" :
                    Header.region = i
                elif char == "X" :
                    if Header.region != 0 :
                        Header.xRay = i
                elif char == "1" :
                    if Header.xRay != 0 :
                        Header.cmRadio = i
                        break
    
    
    @staticmethod
    def cleanHeadersPosition() :
        Header.region = 0
        Header.xRay = 0
        Header.cmRadio = 0


    def printEvents(self) :
        print("\nPRINT EVENTS: ")
        for event in self.events :
            print(event.year + " | " + event.month + " | " + event.day + " | " + event.region + " | " + event.xRay + " | " + event.cmRadio + "\n")


    def clearLists(self) : 
        self.fileLines = list()
        self.events = list()
        SGAS.cleanHeadersPosition()