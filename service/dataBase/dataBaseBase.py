from abc import abstractmethod
class DataBaseBase:
    def __init__(self, connection, table):
        self.__table = table
        self.__connection = connection

        self._onInit()
    
    @abstractmethod
    def _onInit(self):
        pass

    @abstractmethod
    def insert(self, params):
        pass

    @abstractmethod
    def read(self, params):
        pass

    @abstractmethod
    def change(self, params):
        pass

    @property
    def currentTable(self):
        return self.__table

    @property
    def connection(self):
        return self.__connection
