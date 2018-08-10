import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import csv


class AssociationRulesService : 
    originalDataset = "files/dataset.txt"
    classifiedDataset = "files/classifiedDataset"
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
                return "area_small"
            elif area >= 200 and area < 500 : 
                return "area_medium"
            elif area >= 500 and area < 1000 : 
                return "area_large" 
            elif area >=1000 :
                return "area_huge"
        else : 
            return area

    
    def classifySunspot(self, sunspot) : 
        return sunspot.lower().replace("-", "_")

    
    def classifyXray(self, xray) : 
        if xray != "" : 
            return "xray_" + xray[:1]
        else : 
            return xray

    
    def classifyRadio(self, radio) : 
        if radio != "" : 
            radio = int(radio)
            if radio < 80 : 
                return "radio_low"
            elif radio >= 80 and radio < 120 : 
                return "radio_medium"
            elif radio >= 120 and radio < 160 : 
                return "radio_high" 
            elif radio >= 160 :
                return "radio_ultra_high"
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




    def generateAssociationRules(self) : 
        with open(self.transactionalDataset, 'r') as f:
            reader = csv.reader(f)
            dataset = list(reader)

        te = TransactionEncoder()
        te_ary = te.fit(dataset).transform(dataset)
        df = pd.DataFrame(te_ary, columns=te.columns_)

        frequent_itemsets = apriori(df, min_support=0.1, use_colnames=True)
        print(frequent_itemsets)
        print("\n-----------\n")

        rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.1)
        print(rules)

