import sqlite3

class BaseService():
    __conn = None
    __cur = None
    __table = None
    
    def __init__(self, basePath, table):
        self.__table = table
        self.__connection(basePath)
        self.__cur = self.__conn.cursor()

    def __connection(self, basePath):
        self.__conn = sqlite3.connect(basePath, check_same_thread=False)

    def insert(self, params):
        data = self.__parseToInsert(params)

        try :
            self.__cur.execute("INSERT INTO {} VALUES ({});".format(self.__table, data))

            return True
        except sqlite3.IntegrityError as e:
            print('DataBaseBase::insert - ', e)

        return False

    # example: SELECT * FROM users WHERE email='user@gmail.com' and password='mypass'
    # whereParam: "email='user@gmail.com' and password='mypass'"
    def readRow(self, params):
        whereParam = self.__parseToSelect(params)

        self.__cur.execute("SELECT * FROM {} WHERE {}".format(self.__table, whereParam))
        
        return self.__cur.fetchall()

    def commit(self):
        if (not self.__conn): return
            
        self.__conn.commit()

    def close(self):
        if (not self.__conn): return

        self.__conn.close()

        self.__conn = None

    # def saveAndClose(self):
        # self.commit()
        # self.close()


    # value is unpalsle object
    # value example: {'email': ['user@gmail.com'], 'password': ['mypass']}
    # return : "email='user@gmail.com' and password='mypass'"
    def __parseToSelect(self, value):
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

    def __parseToInsert(self, value):
        result = ''
        isFirst = True

        for attr in value:
            attrV = value[attr]

            if (not isFirst):
                result += ','

            if (isinstance(attrV, list)):
                if (len(attrV) != 1):
                    print('   Can not convert attr: {} as {}, because len is {}'.format(attr, attrV, len(attrV)))
                    return None
                else:
                    result += "'" + attrV[0] + "'"
            else:
                result += "'" + str(attrV) + "'"           

            isFirst = False

        return result