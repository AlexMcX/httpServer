from const.pathConst import PathConst
from const.routeConst import RouteConst
from utils.callback import CallBack
from routing.response.badRequestHandler import BadRequestHandler
class Client:    
    def __init__(self):
        self.__user = None
        self.__sLogin = None
        self.__sLogout = None

        self.__onLogin = CallBack()
        self.__onLogout = CallBack()

        self.__routing = None

    @property
    def onLogin(self):
        return self.__onLogin

    @property
    def onLogout(self):
        return self.__onLogout

    def do_GET(self, path, params):
        handler = None

        if not self.__user and \
        (path == PathConst.LOGIN or path == PathConst.AUTHORIZATION):
            auth = RouteConst.ROUTES.get('auth')()

            handler = auth.do_GET(path, params)
            
            if handler.getStatus() == 200:
                self.__user = auth.user

                self.__initRoutes(auth)

            self.__onLogin.fire(self)
        else:
            handler = self.__getHandlerGET(path, params)

            if path == PathConst.LOGOUNT:
                self.__onLogout.fire(self)

        if not handler:
            handler = BadRequestHandler()

        return handler

    def save(self):
        for route in self.__routing:
            route.save()

    def dispose(self):
        pass

    def __getHandlerGET(self, path, params):
        if self.__routing:
            for route in self.__routing:
                result = route.do_GET(path, params)

                if result:
                    return result

        return None

    def __initRoutes(self, auth):
        self.__routing = [auth]

        for path, cl in RouteConst.ROUTES.items():
            if not isinstance(auth, cl):
                self.__routing.append(cl(self.__user))

    @property
    def UUID(self):
        if self.__user:
            return self.__user.uuid

        return None


    