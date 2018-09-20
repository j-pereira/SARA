import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
from datetime import datetime, timedelta
import csv


class AssociationRulesService : 
    originalDataset = "files/dataset.txt"
    classifiedDataset = "files/classifiedDataset.txt"
    transactionalDataset = "files/transactionalDataset.txt"




    def categorizeDataset(self) : 
        _file = open(self.originalDataset)
        filelines = list()

        for line in _file : 
            spl = line.split(",")
            area = ""
            sunspot = ""
            xray = ""
            radio = ""

            for i in range(9) : 
                spl[i] = spl[i].rstrip("\n")
                if i == 4 : 
                    area = self.classifyArea(spl[i])
                if i == 6 : 
                    sunspot = self.classifySunspot(spl[i])
                if i == 7 : 
                    xray = self.classifyXray(spl[i])
                if i == 8 : 
                    radio = self.classifyRadio(spl[i])

            newLine = spl[0] + "," + spl[1] + "," + spl[2] + "," + spl[3] + "," + area + "," + sunspot + "," + xray + "," + radio + "\n"
            filelines.append(newLine)

        _file = open(self.classifiedDataset, 'w')
        _file.writelines(filelines)
        _file.close()


    def classifyArea(self, area) : 
        if area != "" : 
            area = int(area)
            if area < 200 : 
                return "areasmall"
            elif area >= 200 and area < 500 : 
                return "areamedium"
            elif area >= 500 and area < 1000 : 
                return "arealarge" 
            elif area >=1000 :
                return "areahuge"
        else : 
            return area

    
    def classifySunspot(self, sunspot) : 
        return sunspot.lower().replace("-", "")

    
    def classifyXray(self, xray) : 
        if xray != "" : 
            return "xray" + xray[:1]
        else : 
            return xray

    
    def classifyRadio(self, radio) : 
        if radio != "" : 
            radio = int(radio)
            if radio < 80 : 
                return "radiolow"
            elif radio >= 80 and radio < 120 : 
                return "radiomedium"
            elif radio >= 120 and radio < 160 : 
                return "radiohigh" 
            elif radio >= 160 :
                return "radioultra_high"
        else : 
            return radio

    


    def createTransactionalDataset(self) : 
        _file = open(self.classifiedDataset)
        fileLines = list()
        for line in _file : 
            fileLines.append(line)

        fileLines = self.removeDateAndRegion(fileLines)
        fileLines = self.cleanEmptyAttributes(fileLines)
        
        _file = open(self.transactionalDataset, 'w')
        _file.writelines(fileLines)
        _file.close()

    
    def removeDateAndRegion(self, fileLines) : 
        newFileLines = list()
        for line in fileLines : 
            spl = line.split(",")
            newFileLines.append(spl[4] + "," + spl[5] + "," + spl[6] + "," + spl[7])

        return newFileLines 


    def cleanEmptyAttributes(self, fileLines) : 
        newLine = ""
        newFileLines = list()

        for line in fileLines : 
            line = line.split("\n")
            spl = line[0].split(",")

            for i in range(4) : 
                if spl[i] != "":
                    if spl[i] != "\n" : 
                        if newLine != "" :  
                            if newLine[:-1] != "," : 
                                newLine += "," + spl[i]
                            else : 
                                newLine += spl[i]
                        else : 
                            newLine += spl[i]
            newFileLines.append(newLine + "\n")
            newLine = ""
        
        return newFileLines



    def getTransactionalDataset(self) : 
        with open(self.transactionalDataset, 'r') as f:
            reader = csv.reader(f)
            dataset = list(reader)
        return dataset



    def getOriginalDataset(self) : 
        return open(self.originalDataset, 'r' )  
    


    def getClassifiedDataset(self) : 
        return open(self.classifiedDataset, 'r' )  



    def getDatasetByPeriod(self, dataset, lastDateInDataset, holeBase, startYear, startMonth, startDay, endYear, endMonth, endDay, area, sNumber, magClassification, xray, radio) : 
        dataByPeriod = list()
        dataByPeriodAndAttributes = list()

        if not holeBase == "True": 
            dataByPeriod = self.getPeriod(dataset, lastDateInDataset, startYear, startMonth, startDay, endYear, endMonth, endDay)
        else : 
            dataByPeriod = dataset

        if area == "True" and magClassification == "True" and xray == "True" and radio == "True" and (sNumber ==  "True" or sNumber == "none"): 
            dataByPeriodAndAttributes = dataByPeriod
        else : 
            dataByPeriodAndAttributes = self.getAttributes(dataByPeriod, area, sNumber, magClassification, xray, radio)

        return dataByPeriodAndAttributes




    def getPeriod(self, dataset, lastDateInDataset, startYear, startMonth, startDay, endYear, endMonth, endDay) : 
        dataByPeriod = list()
        startDate = datetime.strptime(startYear + startMonth + startDay, "%Y%b%d").date()
        endDate = datetime.strptime(endYear + endMonth + endDay, "%Y%b%d").date()
        firstdate = datetime.strptime("19970101", "%Y%m%d").date()
        lastdate = lastDateInDataset

        if startDate < firstdate : 
            startDate = firstdate
        if endDate > lastdate : 
            endDate = lastdate
        print("Period: " + str(startDate) + " - " + str(endDate))

        for line in dataset : 
            l = line.split(",")
            date = datetime.strptime(l[0] + l[1] + l[2], "%Y%b%d").date()

            if date >= startDate : 
                if date <= endDate : 
                    dataByPeriod.append(line)
            
        return dataByPeriod



    def getAttributes(self, dataset, area, sNumber, magClassification, xray, radio) : 
        if sNumber == "none" : 
            return self.getAttributesForClassifiedDataset(dataset, area, magClassification, xray, radio)
        else : 
            return self.getAttributesForOriginalDataset(dataset, area, sNumber, magClassification, xray, radio)


    def getAttributesForOriginalDataset(self, dataset, area, sNumber, magClassification, xray, radio) : 
        transaction = ""
        dataByAtributes = list()

        for line in dataset : 
            l = line.split(",")
            transaction = l[0] + "," + l[1] + "," + l[2] + "," + l[3] + ","
            if area == "True" :
                transaction += l[4]
            transaction += ","
            if sNumber == "True" : 
                transaction += l[5]
            transaction += ","
            if magClassification == "True" : 
                transaction += l[6]
            transaction += ","
            if xray == "True" : 
                transaction += l[7]
            transaction += ","
            if radio == "True" : 
                transaction += l[8]
            transaction += "\n"
            dataByAtributes.append(transaction)

        return dataByAtributes
    


    def getAttributesForClassifiedDataset(self, dataset, area, magClassification, xray, radio) : 
        transaction = ""
        dataByAtributes = list()

        for line in dataset : 
            l = line.split(",")
            transaction = l[0] + "," + l[1] + "," + l[2] + "," + l[3] + ","
            if area == "True" :
                transaction += l[4]
            transaction += ","
            if magClassification == "True" : 
                transaction += l[5]
            transaction += ","
            if xray == "True" : 
                transaction += l[6]
            transaction += ","
            if radio == "True" : 
                transaction += l[7]
            transaction += "\n"
            dataByAtributes.append(transaction)

        return dataByAtributes




    def generateAssociationRules(self) : 
        dataset = self.getTransactionalDataset()

        te = TransactionEncoder()
        te_ary = te.fit(dataset).transform(dataset)
        df = pd.DataFrame(te_ary, columns=te.columns_)

        frequent_itemsets = apriori(df, min_support=0.1, use_colnames=True)
        print(frequent_itemsets)
        print("\n-----------\n")

        rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.1)
        
        return rules

