import sqlite3
from service.dataBase.dataBaseBase import DataBaseBase

class DataBaseSqlite(DataBaseBase):
    def __init__(self, path):
        self.__conn = None
        self.__cur = None

        super().__init__(path)
    
    def _DataBaseBase__connection(self, path):
        self.__conn = sqlite3.connect(path, check_same_thread=False)

        self.__cur = self.__conn.cursor()

    def insert(self, params):
        data = self.__parseToInsert(params)

        try :
            self.__cur.execute("INSERT INTO {} VALUES ({});".format(super().currentTable, data))

            return True
        except sqlite3.OperationalError as e:
            print('ERROR !!!!!! DataBaseBase::insert - ', e)

        return False

    # example: SELECT * FROM users WHERE email='user@gmail.com' and password='mypass'
    # whereParam: "email='user@gmail.com' and password='mypass'"
    def read(self, params):
        whereParam = self.__parseToSelect(params)
        
        self.__cur.execute("SELECT * FROM {} WHERE {}".format(super().currentTable, whereParam))
        
        values = self.__cur.fetchall()
        
        return self.__createReadResult(values)

    def change(self, params):
        data = self.__parseToChange(params)
        
        if data:
            try:
                self.__cur.execute('''UPDATE {} SET {} WHERE {}'''.format(super().currentTable, data[0], data[1]))

                return True
            except sqlite3.OperationalError as e:
                print('ERROR !!!!!! DataBaseBase::change - ', e)
        
        return False

    def commit(self):
        if (not self.__conn): return
            
        self.__conn.commit()

    def close(self):
        if (not self.__conn): return

        self.__conn.close()

        self.__conn = None

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

            if isinstance(attrV, list):
                for attrVattr in attrV:
                    if (not isFirst):
                        result += " or "
                    result += attr + "='" + attrVattr + "'"

                    isFirst = False
            else:
                result += attr + "='" + attrV + "'" 
        
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
    
    def __parseToChange(self, value):
        if 'changes' in value and 'unique' in value:
            setValue = ''            
            for key in value['changes']:
                setValue += key + '=' + '\'' + str(value['changes'][key]) + '\'' + ','
            
            whereValue = ''
            for key in value['unique']:
                whereValue+= key + '=' + '\'' + str(value['unique'][key]) + '\'' + ','

            setValue = setValue[:len(setValue) - 1]
            whereValue = whereValue[:len(whereValue) - 1]

            return(setValue, whereValue)

        return None

    def __createReadResult(self, values):
        if (len(values) > 0):
            result = {}
            
            names = list(map(lambda x: x[0], self.__cur.description))

            for idx, name in enumerate(names):
                result[name] = values[0][idx]
        
            return result

        return None