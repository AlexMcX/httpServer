import sqlite3

if __name__ == '__main__':
    import baseBase
    bd = baseBase.DataBaseBase('db/userBD.db', 'users')
    bd.readRow("email='t@t' and password='p'")

class DataBaseBase():
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
        self.__cur.execute("INSERT INTO {} VALUES ({});".format(self.__table, params))

    # example: SELECT * FROM users WHERE email='user@gmail.com' and password='mypass'
    # whereParam: "email='user@gmail.com' and password='mypass'"
    def readRow(self, whereParam):
        self.__cur.execute("SELECT * FROM {} WHERE {}".format(self.__table, whereParam))
        
        return self.__cur.fetchall()

    def commit(self):
        self.__conn.commit()

    def close(self):
        self.__conn.close()

    def saveAndClose(self):
        self.commit()
        self.close()