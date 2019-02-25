class BaseVO() :
    # *************** changes data ***************
    def updateChange(self):
        local = locals()
        
        for key in local:
            if (key == 'self'):
                if(not self is '__chahges'):
                    self.__chahges = {}                
                
                for attr, value in local[key].__dict__.items():
                    if attr.find('_BaseVO__'):
                        self.__chahges[attr] = value
        
    def getChangeCampression(self):
        result = {}
        
        result['changes'] = {}
        result['unique'] = self.__getUnique()

        local = locals()

        for key in local:
            if (key == 'self'):
               for attr, value in local[key].__dict__.items():
                   if attr in self.__chahges and self.__chahges[attr] != value:
                       result['changes'][attr] = value


        return result
    # ********************************************


    def getResponse(self):
        var = self.__getResponses()

        if (not var): return None
            
        result = {}

        local = locals()
        
        for k in local:
            if (k == 'self'):                
                for varID in var:
                    for attr, value in local[k].__dict__.items():
                        if (varID == id(value)):
                            result[attr] = value
                            continue

                break

        return result
 
    def __getResponses(self):
        return None
    
    # return object as example :
    # {'uuid':483dc9e6-3132-11e9-8d2b-34e12d6aac5c}
    # to change or save data to database 
    def __getUnique(self):
        return None

            
