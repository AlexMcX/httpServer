class DataBaseBase:
    def __init__(self, path):
        self.__table = None
        self.__connection(path)
    
    def __connection(self, path):
        raise ValueError('Method \'DataBaseBase.__connection\' must be ovveride.')

    def init(self, table):
        self.__table = table

    def insert(self, params):
        raise ValueError('Method \'DataBaseBase.insert\' must be ovveride.')

    def read(self, params):
        raise ValueError('Method \'DataBaseBase.read\' must be ovveride.')

    def change(self, params):
        raise ValueError('Method \'DataBaseBase.change\' must be ovveride.')

    def commit(self):
        raise ValueError('Method \'DataBaseBase.commit\' must be ovveride.')

    def close(self):
        raise ValueError('Method \'DataBaseBase.close\' must be ovveride.')

    @property
    def currentTable(self):
        return self.__table
