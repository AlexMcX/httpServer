from const.restConst import RestConst 
class BaseVO() :
    def __init__(self):
        self.uuid = None

        self.__chahges = {}

    @property
    def readBDData(self):
        return {'uuid':self.uuid}

    # @property
    # def _GETResponseIDS(self):
    #     return [ id(self.uuid) ]
    
    # @property
    # def _POSTResponseIDS(self):
    #     return [ id(self.uuid) ]

    # *************** changes data ***************
    def updateChange(self):
        local = locals()
        
        for key in local:
            if (key == 'self'):               
                for attr, value in local[key].__dict__.items():
                    if attr.find('_BaseVO__'):
                        self.__chahges[attr] = value
        
    def getChangeCompression(self):
        result = {}
        
        result['changes'] = {}
        result['unique'] = self._getUnique()

        local = locals()

        for key in local:
            if (key == 'self'):
               for attr, value in local[key].__dict__.items():
                   if attr in self.__chahges and self.__chahges[attr] != value:
                       result['changes'][attr] = value


        return result
    # ********************************************

    def applyChanges(self, params):
        unique = self._getUnique()

        if not params:
            return

        for key, value in params.items():
            if not key in unique:
                setattr(self, key, value)

    def GETResponse(self):
        return self._createResponse(RestConst.GET)

    # if self is include other response
    def GETResponseSub(self):
        return self._createResponse(RestConst.GET,[]) 
    
    def POSTResponse(self):
        return self._createResponse(RestConst.POST)

    # if self is include other response
    def POSTResponseSub(self):
        return self._createResponse(RestConst.POST,[])

    def _createResponse(self, rest, noIncludeIDS = None):
        result = {}        

        if (noIncludeIDS and len(noIncludeIDS) == 0):
            return result

        # if not includeIDS or (includeIDS and len(includeIDS) > 0):
        local = locals()

        for localKey in local:
            if (localKey == 'self'):
                for attr, value in local[localKey].__dict__.items():                        
                    if not noIncludeIDS or (noIncludeIDS and not id(attr) in noIncludeIDS):                            
                        if value and value != self.__chahges:
                            if isinstance(value, BaseVO):
                                if rest == RestConst.GET:
                                    result[attr] = value.GETResponseSub()
                                else:
                                    result[attr] = value.POSTResponseSub()
                            else:
                                result[attr] = value

            else:
                break

        return result
    
    def _getUnique(self):
         return {'uuid':self.uuid}

            
