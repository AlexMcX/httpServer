from abc import abstractmethod

class RequestHandler():
    def __init__(self):
        self.__contents = None

    def getContents(self):
        return self.__contents        

    def setContents(self, value):
        self.__contents = value

    @abstractmethod
    def getStatus(self):
        pass

    @abstractmethod
    def getContentType(self):
        pass

    def getType(self):
        return 'static'