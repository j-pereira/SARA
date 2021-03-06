from flask_restful import Resource, Api, reqparse
from datasetService import DatasetService
from associationRulesService import AssociationRulesService
import pandas as pd
import json
import csv
import re

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



class OriginalDataset(Resource) : 

    def get(self) : 
        datasetService = DatasetService()
        associationRulesService = AssociationRulesService()

        dataset = associationRulesService.getOriginalDataset()
        reader = csv.DictReader(dataset, fieldnames = ('year','month','day','region', 'area', 'sNumber', 'magClassification', 'xray', 'radio'))  
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
        parser.add_argument('sNumber')
        parser.add_argument('magClassification')
        parser.add_argument('xray')
        parser.add_argument('radio')
        args = parser.parse_args()
        
        datasetService = DatasetService()
        associationRulesService = AssociationRulesService()
        datasetService.setLastDateInDataset()

        originalDataset = associationRulesService.getOriginalDataset()
        dataset = associationRulesService.getDatasetByPeriod(originalDataset, datasetService.lastDateInDataset, args.holeBase, args.startYear, args.startMonth, args.startDay, args.endYear, args.endMonth, args.endDay, args.area, args.sNumber, args.magClassification, args.xray, args.radio)

        reader = csv.DictReader(dataset, fieldnames = ('year','month','day','region', 'area', 'sNumber', 'magClassification', 'xray', 'radio'))  
        out = json.dumps( [ row for row in reader ] )  
        
        return json.loads(out)




class ClassifiedDataset(Resource) : 

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
        parser.add_argument('sNumber')
        parser.add_argument('magClassification')
        parser.add_argument('xray')
        parser.add_argument('radio')
        args = parser.parse_args()
        
        datasetService = DatasetService()
        associationRulesService = AssociationRulesService()
        datasetService.setLastDateInDataset()

        associationRulesService.categorizeDataset()
        classifiedDataset = associationRulesService.getClassifiedDataset()
        dataset = associationRulesService.getDatasetByPeriod(classifiedDataset, datasetService.lastDateInDataset, args.holeBase, args.startYear, args.startMonth, args.startDay, args.endYear, args.endMonth, args.endDay, args.area, args.sNumber, args.magClassification, args.xray, args.radio)

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

        regex = re.compile(r'\bInfinity\b',flags=re.IGNORECASE)
        sub = re.sub(regex, ' \"Infinity\" ', out)

        return json.loads(sub)
    

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
        parser.add_argument('sNumber')
        parser.add_argument('magClassification')
        parser.add_argument('xray')
        parser.add_argument('radio')
        parser.add_argument('support')
        parser.add_argument('confidence')
        args = parser.parse_args()
        
        datasetService = DatasetService()
        associationRulesService = AssociationRulesService()
        datasetService.setLastDateInDataset()
        associationRulesService.categorizeDataset()
        classifiedDataset = associationRulesService.getClassifiedDataset()
        dataset = associationRulesService.getDatasetByPeriod(classifiedDataset, datasetService.lastDateInDataset, args.holeBase, args.startYear, args.startMonth, args.startDay, args.endYear, args.endMonth, args.endDay, args.area, args.sNumber, args.magClassification, args.xray, args.radio)
        associationRulesService.saveTempClassifiedDataset(dataset)
        associationRulesService.createTransactionalDatasetByTemp()
        rules = associationRulesService.generateAssociationRules(args.support, args.confidence)
        print(rules)

        out = json.dumps(rules.to_dict(), default=dumper)
        regex = re.compile(r'\bInfinity\b', flags=re.IGNORECASE)
        sub = re.sub(regex, ' \"Infinity\" ', out)
        
        regex1 = re.compile(r'\bfrozenset\b', flags=re.IGNORECASE)
        sub1 = re.sub(regex1, ' ', sub)

        return json.loads(sub1)

