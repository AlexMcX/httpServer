from const.pathConst import PathConst
from utils.callback import CallBack
from database.baseUser import DataBaseUser
from response.staticHandler import StaticHandler
from response.templateHandler import TemplateHandler
from response.badRequestHandler import BadRequestHandler

class Client:    
    def __init__(self):
        self.__dbUser = DataBaseUser()
        self.__sLogin = None
        self.__sLogout = None

        self.__onLogin = CallBack()
        self.__onLogout = CallBack()

        self.__getPath = {
                PathConst.LOGIN             :   self.__dbUser.login,
                PathConst.AUTHORIZATION     :   self.__dbUser.register,
                PathConst.LOGOUNT           :   self.__dbUser.logOut
        }

    @property
    def onLogin(self):
        return self.__onLogin

    @property
    def onLogout(self):
        return self.__onLogout

    def do_GET(self, path, params):
        call = self.__getPath.get(path)

        if (call):
            handler = call(params)
        else:
            handler = BadRequestHandler()

            print('Undefined client command: {}'.format(path))
        
        if path == PathConst.LOGIN or path == PathConst.AUTHORIZATION:
            self.__onLogin.fire(self)
        elif path == PathConst.LOGOUNT:
            self.__onLogout.fire(self)

        self.__dbUser.updateLastVisit()

        return handler

    def save(self):
        self.__dbUser.save()

    @property
    def UUID(self):
        return self.__dbUser.getUUID


    