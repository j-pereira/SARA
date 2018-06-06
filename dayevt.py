import urllib.request
from header import Header
from event import Event

class DayEvt:
    fileName = "20140109SGAS"
    extension = ".txt"
    urlPath = fileName + extension
    filePath = "files/" + fileName + extension
    fileLines = list()
    events = list()


    
    def download(self, url) :
        urllib.request.urlretrieve(url + self.urlPath, self.filePath)

    def openFile(self) :
        return open(self.filePath)

    def readFile(self, _file) :
        for line in _file:
            self.fileLines.append(line)
    
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

            if lineSplited[0] == ":Issued:" :
                year = lineSplited[1]
                month = lineSplited[2]
                day = lineSplited[3]
            
            if flag == True :
                if line == "No Data.\n" :
                    break
                else : 
                    event = Event()
                    event.year = year
                    event.month = month
                    event.day = day
                    event.region = DayEvt.findAttribute(line, "region")
                    event.xRay = DayEvt.findAttribute(line, "xray")
                    event.cmRadio = DayEvt.findAttribute(line, "radio")
                    if (event.region != "") and ((event.xRay != "") or (event.cmRadio != "")) : 
                        self.events.append(event)

            if lineSplited[0] == "#Begin" :
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
        
        print("Flag: " + flag + " - Cont: " + str(cont))

        while line[cont] != " " :
            cont = cont - 1

        pos = cont + 1
        while line[pos] != " " :
            attribute += line[pos]
            pos += 1
        
        print("Attribute: " + attribute)
        return attribute


    

    def loadFilesHeader(self) :
        header = ""
        for line in self.fileLines : 
            lineSplited = line.split(" ")
            if lineSplited[0] == "#Begin" : 
                header = line
                break
        print("Headers line == : " + line)
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
        print("Region: " + str(Header.region))
        print("Xray: " + str(Header.xRay))
        print("Radio: " + str(Header.cmRadio))
    
    
    def cleanHeadersPosition(self) :
        Header.region = 0
        Header.xRay = 0
        Header.cmRadio = 0


    def printEvents(self) :
        print("\n PRINT EVENTS: ")
        for event in self.events :
            print(event.year + " | " + event.month + " | " + event.day + " | " + event.region + " | " + event.xRay + " | " + event.cmRadio + "\n")