import time
import uuid
from utils.objectEx import *
from database.vo.userVO import UserVO
from routing.auth.response.loginRequestHandler import LoginRequestHandler
from routing.auth.response.registerRequestHandler import RegisterRequestHandler
from routing.auth.response.logOutRequestHandler import LogOutRequestHandler
from service.dataBaseService import DataBaseService
from routing.route import Route
from const.pathConst import PathConst

class AuthRoute(Route):
    def __init__(self):
        self.__uuid = None
        self.__userBD = DataBaseService.getInstance().users

        super().__init__(None)

    def do_GET(self, path, params):
        self.__updateLastVisit()

        return super().do_GET(path, params)

    def save(self):
        saveData = self.user.getChangeCampression()

        self.__userBD.change(saveData)

    @property
    def getUUID(self):
        return self.__uuid

    def _routing(self):
        return {
                PathConst.LOGIN             :   self.__login,
                PathConst.AUTHORIZATION     :   self.__register,
                PathConst.LOGOUNT           :   self.__logOut        
        }

    def __login(self, params):
        result = LoginRequestHandler()

        self.__setCurrentUser(params)

        if(not self.user):
            result.setContentsUserNotExist()

            return result

        result.setContentsSuccess(self.user.getLoginResponse())

        return result

    def __register(self, params):
        result = RegisterRequestHandler()

        result.setContentsUserExist()

        if(self.user):
            return result
        
        # create new user if user not exist in base
        isCreateUser = self.__createUser(params)
        
        if (isCreateUser):
            self.__setCurrentUser(params)

            result.setContentsSuccess(self.user.getLoginResponse())           

        return result

    def __logOut(self, params):
        result = LogOutRequestHandler()

        if (isEqualFields(params, self.user)):
            result.setContentsSuccessfully()

            return result

        result.setContentsUserNotExist()

        return result

    # format insert bd - "uuid, email, password, createtime"
    def __createUser(self, params):
        if (params):
            insert = params.copy()

            insert['icon'] = ''
            insert['uuid'] = str(uuid.uuid1())
            insert['time'] = time.time()
            insert['lastvisittime'] = time.time()

            isInsert = self.__userBD.insert(insert)
            
            if (isInsert) :
                self.__userBD.commit()

                return True

        return False

    def __setCurrentUser(self, params):
        if self.user: return

        dbUser = self.__userBD.read(params)
        
        self._Route__user = createObjectFromBD(UserVO, dbUser)

        if self.user:
            self.__uuid = self.user.uuid

    def __updateLastVisit(self):
        if self.user:
            self.user.lastvisittime = time.time()