def getAllPublicVars(cl):
    result = []
    for attr, value in cl.__dict__.items():
        if(attr.find('_CONST') == -1 and attr.find('__') == -1):
            result.append(attr)
    
    return result
            
# cl - class new instance
# dbData - data from dataBase, as object
def createObjectFromBD(cl, dbData):   
    if dbData:
        inst = cl() 

        for field in dbData:
            if field in inst.__dict__:
                inst.__dict__[field] = dbData[field]
            
        inst.updateChange()

        return inst
    return None

# registration:  {'email': ['a@t'], 'password': ['p']}
# '{}','{}','{}','{}'
def prsetoSqliteInsert(value):
    result = ''
    isFirst = True

    for attr in value:
        attrV = value[attr]

        if (len(attrV) != 1):
            return None

        if (not isFirst):
            result += ','

        result += "'" + attrV[0] + "'"        

        isFirst = False

    return result

# json example: {'uuid': ['373b2b48-2adc-11e9-a924-34e12d6aac5b']}
# inst is instans of class : UserVO, ......
def isEqualFields(json, inst):
    if not json or not inst or len(json) == 0:
        return False

    for field in json:
        if json[field] != inst.__dict__[field]:
            if type(json[field]) is list and len(json[field]) == 1:
                if json[field][0] == inst.__dict__[field]:
                    continue
            return False
        
    return True
    
def getCommonFields(json, cl):   
    result = {}
    inst = cl()
    params = getAllPublicVars(inst)
    
    for val in params:
        if val in json:
            result[val] = json[val]

    inst = None

    return result