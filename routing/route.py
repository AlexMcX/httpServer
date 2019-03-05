from abc import abstractmethod

class Route:
    def __init__(self, user):
        self.__user = user
    
    def request(self, path, params):
        call = self._routing().get(path)

        if call:
            return call(params)

        return None

    @property
    def user(self):
        return self.__user

    @abstractmethod
    def _routing(self):
        pass

    @abstractmethod
    def save(self):
        pass
