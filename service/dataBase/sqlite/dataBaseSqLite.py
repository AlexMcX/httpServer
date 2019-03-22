import sqlite3
from service.dataBase.dataBaseBase import DataBaseBase

class DataBaseSqlite(DataBaseBase):
    def __init__(self, connection, table):
        self.__conn = None
        self.__cur = None
        self.__columns = None

        super().__init__(connection, table)
    
    def _onInit(self):
        self.__cur = super().connection.cursor()

        self.__cur.execute('SELECT * FROM {}'.format(super().currentTable))
        self.__columns = list(map(lambda x: x[0], self.__cur.description))

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
        readParams = self.__createRead(params)

        whereParam = self.__parseToSelect(readParams)
        
        try:
            if readParams and whereParam:
                self.__cur.execute("SELECT * FROM {} WHERE {}".format(super().currentTable, whereParam))
            
                values = self.__cur.fetchall()
            
                return self.__createReadResult(values)
        except sqlite3.OperationalError as e:
            print('          <<<<<<<<<< ERROR !!!!!! DataBaseBase::read !!!!!! >>>>>>>>>>')
            print('          Error: ', e)
            print('          Params:', params)
            print('          ReadParams:', readParams)
            print('          WhereParam: ', whereParam)
            print('          Table: ', self.currentTable)

        return None

    def change(self, params):
        data = self.__parseToChange(params)

        if data:
            print("    DB SET: to table:", self.currentTable, " params (", data[0], ")")
            try:
                self.__cur.execute('''UPDATE {} SET {} WHERE {}'''.format(super().currentTable, data[0], data[1]))

                return True
            except sqlite3.OperationalError as e:
                print('          <<<<<<<<<< ERROR !!!!!! DataBaseBase::change !!!!!! >>>>>>>>>>')
                print('          Error: ', e)
                print('          Params:', params)
                print('          Table: ', self.currentTable)
        
        return False

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

            changes = value['changes']

            for key in changes:
                if key in self.__columns:
                    setValue += key + '=' + '\'' + str(changes[key]) + '\'' + ','
            
            whereValue = ''
            for key in value['unique']:
                whereValue+= key + '=' + '\'' + str(value['unique'][key]) + '\'' + ','

            setValue = setValue[:len(setValue) - 1]
            whereValue = whereValue[:len(whereValue) - 1]

            if setValue and whereValue:
                return(setValue, whereValue)

        return None

    def __createRead(self, params):
        if params:
            result = {}

            for value in params:
                if value in self.__columns:
                    result[value] = params[value]

            return result
        return None

    def __createReadResult(self, values):
        if (len(values) > 0):
            result = {}

            for idx, column in enumerate(self.__columns):
                result[column] = values[0][idx]
        
            return result

        return None
