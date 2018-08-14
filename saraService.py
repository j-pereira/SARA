import pandas as pd
from datasetService import DatasetService
from associationRulesService import AssociationRulesService
import csv

class SARA : 

    def getAssociationRules (self) : 
        datasetService = DatasetService()
        datasetService.setLastDateInDataset()

        '''
        if not datasetService.isDatasetUpdated() : 
            datasetService.updateDataset()
        '''
        associationRulesService = AssociationRulesService()
        associationRulesService.categorizeDataset()
        associationRulesService.createTransactionalDataset()
        rules = associationRulesService.generateAssociationRules()
        print(rules)
        
        '''rules.to_csv("files/rulesToCsv.csv", sep=',')

        with open('files/rulesToCsv.csv', mode='r') as infile:
            reader = csv.reader(infile)
            with open('files/rulesToCsv_new.csv', mode='w') as outfile:
                writer = csv.writer(outfile)
                mydict = {rows[0]:rows[1] for rows in reader}

        print(mydict)'''

        return rules