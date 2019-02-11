def getAllPublicVars(cl):
    result = []

    for attr, value in cl.__dict__.items():
        if(attr.find('_CONST') == -1 and attr.find('__') == -1):
            result.append(attr)
    
    return result
            
# cl - class new instance
#  readFunc - function read from bd with parameters (fieldName, filterName, filter)
# [('373b2b48-2adc-11e9-a924-34e12d6aac5b', 't@t', 'p', 1549546091.930708)]
def createObjectFromBD(cl, dbData):
    inst = cl()
    params = getAllPublicVars(cl)

    if (len(dbData) != 0):
        for idx, val in enumerate(params):
            inst.__dict__[val] = dbData[0][idx]
        
        return inst
    return None

# value is unpalsle object
# value example: {'email': ['user@gmail.com'], 'password': ['mypass']}
# return : "email='user@gmail.com' and password='mypass'"
def parseToSqliteSelect(value):
    result = ''
    attrV = None
    isFirst = None
    
    for attr in value:
        attrV = value[attr]
        
        isFirst = True
        
        if (result.strip()):
            result += ' and '

        for attrVattr in attrV:
            if (not isFirst):
                result += " or "
            result += attr + "='" + attrVattr + "'"

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