from flask_restful import Resource, Api
import pandas as pd
from saraService import SARA
import json
import csv

class FrozensetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, frozenset) : 
            elements = list()
            for i in range(len(obj)) : 
                x, *_ = obj
                elements.append(x)
                print(elements)
            '''
            x = ""
            for i in range(len(elements)) : 
                if i != 0 : 
                    x += "," + elements[i]
                else : 
                    x += elements[i]
            '''
            print(x)
            return x
        else :   
            return json.JSONEncoder.default(self, obj)



def dumper(obj):
    try:
        return obj.toJSON()
    except:
        '''
        for i in range(len(obj)) : 
            j = ""
            if isinstance(obj, frozenset) : 
                n, *_ = obj
                m = {'obj': n}
                print(m)
            j += str(m)'''

        '''x = obj['antecedants']
        x += obj['support']
        x += obj['antecedant support']
        x += obj['consequent support']
        x += obj['support']
        x += obj['consequent']
        '''

        return str(obj)



class AssociationRules(Resource) :

    def get(self) : 
        
        sara = SARA()
        rules = sara.getAssociationRules()

        #_json = json.dumps(rules, cls=FrozensetEncoder)
      
        return json.dumps(rules.to_dict(), default=dumper)
