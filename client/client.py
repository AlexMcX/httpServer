from database.baseUser import DataBaseUser
from response.staticHandler import StaticHandler
from response.templateHandler import TemplateHandler
from response.badRequestHandler import BadRequestHandler

class Client:
    __dbUser = DataBaseUser()

    __getPath = {
            '/login'    :   __dbUser.login,
            '/auth'     :   __dbUser.register,
            '/logout'   :   __dbUser.logOut
        }

    def do_GET(self, path, params):
        call = self.__getPath.get(path)

        if (call):
            handler = call(params)
        else:
            handler = BadRequestHandler()

            print('Undefined client command: {}'.format(path))

        return handler

    def save(self):
        self.__dbUser.commit()
        self.__dbUser.close()

    def getUUID(self):
        return self.__dbUser.getUUID()

    