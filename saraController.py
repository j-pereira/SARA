from flask_restful import Resource, Api, reqparse
from datasetService import DatasetService
from associationRulesService import AssociationRulesService
import pandas as pd
import json
import csv


def dumper(obj):
    try:
        return obj.toJSON()
    except:
        return str(obj)


class UpdateDataset(Resource) : 

    def get(self) : 
        datasetService = DatasetService()
        associationRulesService = AssociationRulesService()
        datasetService.setLastDateInDataset()
        if not datasetService.isDatasetUpdated() : 
            datasetService.updateDataset()
            datasetService.setLastDateInDataset()
        out = json.dumps({
            'data': str(datasetService.lastDateInDataset),
            'updated': datasetService.isDatasetUpdated()
        })
        return json.loads(out)
    



class LastDateDataset(Resource) : 

    def get(self) : 
        datasetService = DatasetService()
        associationRulesService = AssociationRulesService()
        datasetService.setLastDateInDataset()
        out = json.dumps({
            'data': str(datasetService.lastDateInDataset),
            'updated': datasetService.isDatasetUpdated()
        })
        return json.loads(out)



class DatasetController(Resource) : 

    def get(self) : 
        datasetService = DatasetService()
        associationRulesService = AssociationRulesService()
        
        associationRulesService.categorizeDataset()
        dataset = associationRulesService.getClassifiedDataset()
        reader = csv.DictReader(dataset, fieldnames = ('year','month','day','region', 'area', 'magClassification', 'xray', 'radio'))  
        out = json.dumps( [ row for row in reader ] )  
        
        return json.loads(out)
    

    def post(self) : 
        parser = reqparse.RequestParser()
        parser.add_argument('holeBase')
        parser.add_argument('startYear')
        parser.add_argument('startMonth')
        parser.add_argument('startDay')
        parser.add_argument('endYear')
        parser.add_argument('endMonth')
        parser.add_argument('endDay')
        parser.add_argument('area')
        parser.add_argument('magClassification')
        parser.add_argument('xray')
        parser.add_argument('radio')
        args = parser.parse_args()
        

        datasetService = DatasetService()
        associationRulesService = AssociationRulesService()
        
        associationRulesService.categorizeDataset()
        dataset = associationRulesService.getClassifiedDatasetByPeriod(args.holeBase, args.startYear, args.startMonth, args.startDay, args.endYear, args.endMonth, args.endDay, args.area, args.magClassification, args.xray, args.radio)

        reader = csv.DictReader(dataset, fieldnames = ('year','month','day','region', 'area', 'magClassification', 'xray', 'radio'))  
        out = json.dumps( [ row for row in reader ] )  
        
        return json.loads(out)



class AssociationRulesController(Resource) :

    def get(self) : 
        associationRulesService = AssociationRulesService()
        associationRulesService.createTransactionalDataset()
        rules = associationRulesService.generateAssociationRules()
        print(rules)
        out = json.dumps(rules.to_dict(), default=dumper)
        
        return json.loads(out)
