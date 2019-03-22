from abc import abstractmethod

class Route:
    __routing = None

    def __init__(self, user):
        self.__user = user

        self.__routing = self._routing()

        self._onInit() 

    def dispose(self):
        self.save()

        self._onDisposee()

        self.__user = None
        self.__routing = None        

    def request(self, path, rest, params):
        restCalls = self.__routing.get(rest)
        
        if restCalls:
            call = restCalls.get(path)
            
            if call:                
                return call(params)

        return None

    @property
    def user(self):
        return self.__user

    def _onInit(self):
        pass    

    @abstractmethod
    def _onDisposee(self):
        pass

    @abstractmethod
    def _routing(self):
        pass

    @abstractmethod
    def save(self):
        pass
