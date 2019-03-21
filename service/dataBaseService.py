class DataBaseService:
    SQLITE3 = 'sqlite3'
    CUSTOMER_DATA_BASE = ('db/userBD.db', 'customer')
    PROFILE_DATA_BASE = ('db/userBD.db', 'profile')

    __instance = None
    __type = SQLITE3
    __bds = {}

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
        for keyS, bds in DataBaseService.__bds.items():
            for key, bd in bds.items():
                bd.commit()
                bd.close()

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

        result.init(data[1])
        
        return result

    def __getBD(self, bdType):
        if bdType[0] in DataBaseService.__bds:
            if(bdType[1] in bdType[0]):
                return DataBaseService.__bds[bdType[0]][bdType[1]]
        return None

    def __createBD(self, bdType):
        result = None

        if (DataBaseService.__type == DataBaseService.SQLITE3):
            from service.dataBase.sqlite.dataBaseSqLite import DataBaseSqlite

            result = DataBaseSqlite(bdType[0])

            if not bdType[0] in DataBaseService.__bds:
                DataBaseService.__bds[bdType[0]] = {}

            DataBaseService.__bds[bdType[0]][bdType[1]] = result

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
        