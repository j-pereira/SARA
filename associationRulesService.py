import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import csv


class AssociationRulesService : 
    originalDatasetFile = "files/dataset.txt"
    transactionalDatasetFile = "files/transactionalDataset.txt"




    def categorizeDataset(self) : 
        _file = open(self.originalDatasetFile)
        filelines = list()

        for line in _file : 
            spl = line.split(",")
            area = ""
            sunspot = ""
            xray = ""
            radio = ""

            for i in range(9) :
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

        _file = open("files/transaction.txt", 'w')
        _file.writelines(filelines)
        _file.close()





    
    def classifyArea(self, area) : 
        if area != "" : 
            area = int(area)
            if area < 200 : 
                return "areapequena"
            else if area >= 200 and area < 500 : 
                return "areamoderada"
            else if area >= 500 and area < 1000 : 
                return "areagrande" 
            else if area >=1000 :
                return "areagigantesca"
        else : 
            return area

    
    def classifySunspot(self, sunspot) : 
        return sunspot.lower()
    
    def classifyXray(self, xray) : 
        if xray != "" : 
            if xray[:1] == "A" : 
            return "xrayA"
            else if xray[:1] == "B" :
                return "xrayB"
            else if xray[:1] == "C" : 
                return "xrayC"
            else if xray[:1] == "M" :
                return "xrayM"
            else if xray[:1] == "X" : 
                return "xrayX"
        else : 
            return xray

    
    def classifyRadio(self, radio) :
        return ""

    


    def createTransactionalDataset(self) : 

        _file = open(self.originalDatasetFile)

        newLine = ""
        fileLines = list()

        for line in _file : 
            spl = line.split(",")
            for i in range(9) : 
                if spl[i] != "":
                    if spl[i] != "\n" : 
                        if i != 0 :
                            newLine += "," + spl[i]
                        else : 
                            newLine += spl[i]
            fileLines.append(newLine)
            newLine = ""
        
        for line in fileLines : 
            print(line)





    def generateAssociationRules(self) : 
        _file = open('files/dataset.txt')

        with open('files/dataset.txt', 'r') as f:
            reader = csv.reader(f)
            dataset = list(reader)

        print(dataset)
        print("-----------\n")

        te = TransactionEncoder()
        te_ary = te.fit(dataset).transform(dataset)
        df = pd.DataFrame(te_ary, columns=te.columns_)

        print(df)
        print("-----------\n\n")

        frequent_itemsets = apriori(df, min_support=0.1, use_colnames=True)
        print(frequent_itemsets)
        print("-----------\n\n")

        rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.5)
        print(rules)

