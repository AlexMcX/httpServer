from abc import abstractmethod
class DataBaseBase:
    def __init__(self, connection, table):
        self.__table = table
        self.__connection = connection
        # self._connection(path)

        self._onInit()
    
    # @abstractmethod
    # def _connection(self, path):
    #     pass
    
    @abstractmethod
    def _onInit(self):
        pass
        # self.__table = table

    @abstractmethod
    def insert(self, params):
        pass

    @abstractmethod
    def read(self, params):
        pass

    @abstractmethod
    def change(self, params):
        pass

    # @abstractmethod
    # def commit(self):
    #     pass

    # @abstractmethod
    # def close(self):
    #     pass

    @property
    def currentTable(self):
        return self.__table

    @property
    def connection(self):
        return self.__connection
