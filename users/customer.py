# from const.pathConst import PathConst
from const.routeConst import RouteConst
# from utils.callback import CallBack
# from routing.response.badRequestHandler import BadRequestHandler
from users.user import User

class Customer(User):
    def __init__(self):
        super().__init__()
    
    @property
    def _routes(self):
        return RouteConst.USER_ROUTES

    # def __init__(self):
        # self.__user = None
        # self.__sLogin = None
        # self.__sLogout = None

        # self.__onLogin = CallBack()
        # self.__onLogout = CallBack()

        # self.__routing = None

    # @property
    # def onLogin(self):
    #     return self.__onLogin

    # @property
    # def onLogout(self):
    #     return self.__onLogout

    # def request(self, path, rest, params):
    #     handler = None

    #     if not self.__user and path == PathConst.AUTHORIZATION:
    #         auth = getRoutes.get('auth')()

    #         handler = auth.request(path, rest, params)
            
    #         if handler.getStatus() == 200:
    #             self.__user = auth.user

    #             self.__initRoutes(auth)

    #         self.__onLogin.fire(self)
    #     else:
    #         handler = self.__getRequestHandler(path, rest, params)

    #         if path == PathConst.LOGOUNT and handler:
    #             self.__onLogout.fire(self)

    #     if not handler:
    #         handler = BadRequestHandler()

    #     return handler

    # def save(self):
    #     for route in self.__routing:
    #         route.save()

    # def dispose(self):
    #     pass

    # def __getRequestHandler(self, path, rest, params):
    #     if self.__routing:
    #         for route in self.__routing:
    #             result = route.request(path, rest, params)

    #             if result:
    #                 return result

    #     return None

    # def __initRoutes(self, auth):
    #     self.__routing = [auth]

    #     for path, cl in RouteConst.ROUTES.items():
    #         if not isinstance(auth, cl):
    #             self.__routing.append(cl(self.__user))

    # @property
    # def __routes(self):
    #     return RouteConst.USER_ROUTES

    # @property
    # def UUID(self):
    #     if self.__user:
    #         return self.__user.uuid

    #     return None


    