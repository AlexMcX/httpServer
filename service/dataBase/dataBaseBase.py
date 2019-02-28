from abc import abstractmethod
class DataBaseBase:
    def __init__(self, path):
        self.__table = None
        self.__connection(path)
    
    @abstractmethod
    def __connection(self, path):
        pass
    
    def init(self, table):
        self.__table = table

    @abstractmethod
    def insert(self, params):
        pass

    @abstractmethod
    def read(self, params):
        pass

    @abstractmethod
    def change(self, params):
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @property
    def currentTable(self):
        return self.__table
