class BaseVO() :
    def getResponse(self):
        var = self.__getResponses__()

        if (not var): return None
            
        result = {}

        local = locals()
        
        for k in local:
            if (k == 'self'):                
                for varID in var:
                    for attr, value in local[k].__dict__.items():
                        if (varID == id(value)):
                            # result += '\'' + attr + '\'' + ':' + value + ','
                            result[attr] = value
                            continue

                break

        # result = result[0:len(result) - 1]

        # result += "}"

        return result
 
    def __getResponses__(self):
        return None
            