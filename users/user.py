from utils.callback import CallBack
from abc import abstractmethod
from const.routeConst import RouteConst
from const.pathConst import PathConst
from routing.response.badRequestHandler import BadRequestHandler

class User:
    def __init__(self):
        self.__user = None

        self.__sLogin = None
        self.__sLogout = None

        self.__routing = None

        self.__onLogin = CallBack()
        self.__onLogout = CallBack()
    
    @property
    def onLogin(self):
        return self.__onLogin

    @property
    def onLogout(self):
        return self.__onLogout

    @property
    def UUID(self):
        if self.__user:
            return self.__user.uuid

        return None

    @property
    @abstractmethod
    def _routes(self):
        pass

    def request(self, path, rest, params):
        handler = None

        if not self.__user and path == PathConst.AUTHORIZATION:
            auth = self._routes.get('auth')()

            handler = auth.request(path, rest, params)
            
            if handler:
                if handler.getStatus() == 200:
                    self.__user = auth.user

                    self.__initRoutes(auth)

            self.__onLogin.fire(self)
        else:
            handler = self.__getRequestHandler(path, rest, params)

            if path == PathConst.LOGOUNT and handler:
                self.__onLogout.fire(self)

        if not handler:
            handler = BadRequestHandler()

        return handler

    def save(self):
        for route in self.__routing:
            route.save()

    def dispose(self):
        pass

    def __getRequestHandler(self, path, rest, params):
        if self.__routing:
            for route in self.__routing:
                result = route.request(path, rest, params)

                if result:
                    return result

        return None

    def __initRoutes(self, auth):
        self.__routing = [auth]

        for path, cl in self._routes.items():
            if not isinstance(auth, cl):
                self.__routing.append(cl(self.__user))

    

    
    