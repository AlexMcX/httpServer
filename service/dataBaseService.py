class DataBaseService:
    SQLITE3 = 'sqlite3'
    CUSTOMER_DATA_BASE = ('db/userBD.db', 'customer')
    PROFILE_DATA_BASE = ('db/userBD.db', 'profile')

    __instance = None
    __type = SQLITE3
    __bds = {}                  # {connection:..., cursors:...}, 
                                # connection is connection to bd
                                # cursors is instances of bd classes
                                # example cursors {tableName:instance}

    @staticmethod
    def setTypeBase(typeBD):
        DataBaseService.__type = typeBD

    @staticmethod
    def getInstance():
      """ Static access method. """
      if DataBaseService.__instance == None:
         DataBaseService()
      return DataBaseService.__instance
    
    @staticmethod
    def commitAndClose():
        for keyS, data in DataBaseService.__bds.items():
            if "connection" in data:
                connection = data["connection"]

                if connection:
                    connection.commit()
                    connection.close()

    def __init__(self):
      """ Virtually private constructor. """
      if DataBaseService.__instance != None:
         raise Exception("This class is a singleton!")
      else:
         DataBaseService.__instance = self

    @property
    def clients(self):
        return self.__initBD(DataBaseService.CUSTOMER_DATA_BASE)

    @property
    def profile(self):
        return self.__initBD(DataBaseService.PROFILE_DATA_BASE)

    def __initBD(self, data):
        result = self.__getBD(data)
        
        if not result:
            result = self.__createBD(data)

        # result.init(data[1])
        
        return result

    def __getBD(self, bdType):
        if bdType[0] in DataBaseService.__bds:
            cursors = DataBaseService.__bds[bdType[0]]["cursors"]

            if (bdType[1] in cursors):
                return cursors[bdType[1]]
        return None

    def __createBD(self, bdType):
        result = None

        if DataBaseService.__type == DataBaseService.SQLITE3:
            import sqlite3
            from service.dataBase.sqlite.dataBaseSqLite import DataBaseSqlite

            connection = None            

            if not bdType[0] in DataBaseService.__bds:
                connection = sqlite3.connect(bdType[0], timeout = 10, check_same_thread=False)

                DataBaseService.__bds[bdType[0]] = {
                    "connection" : connection,
                    "cursors":{}
                }
            else:
                connection = DataBaseService.__bds[bdType[0]]["connection"]

            result = DataBaseSqlite(connection, bdType[1])

            if not bdType[1] in DataBaseService.__bds[bdType[0]]["cursors"]:
                DataBaseService.__bds[bdType[0]]["cursors"] = {bdType[1]:result}

        return result















    # def insert(self, params):
    #     pass

    # def read(self, params):
    #     pass

    # def change(self, params):
    #     pass

    # def commit(self):
    #     pass

    # def close(self):
    #     pass
        