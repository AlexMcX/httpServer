# if __name__ == '__main__':
#     import baseBase
#     bd = baseBase.DataBaseBase('db/userBD.db', 'users')
#     bd.readRow("email='t@t' and password='p'")

class DataBaseBase():    
    SQLITE3 = 'sqlite3'
    
    __service = None

    def __init__(self, baseType, basePath, table):
        if(baseType == self.SQLITE3):
            from database.sqlite3.baseService import BaseService

            self.__service = BaseService(basePath, table)

    # params is dict, 
    # Example:
    # {'email': ['myemail@gmail.com'], 'password': ['mypassword']} 
    # or
    # {'email': 'myemail@gmail.com', 'password': 'mypassword'}
    def insert(self, params):
        return self.__service.insert(params)

    # params is dict, 
    # Example:
    # {'email': ['myemail@gmail.com'], 'password': ['mypassword']} 
    # or
    # {'email': 'myemail@gmail.com', 'password': 'mypassword'}
    def readRow(self, params):
        return self.__service.readRow(params)

    def commit(self):
        self.__service.commit()

    def close(self):
        self.__service.close()