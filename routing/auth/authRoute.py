import time
import uuid
from abc import abstractmethod
from utils.objectEx import *
from database.vo.customerVO import CustomerVO
from routing.auth.response.loginRequestHandler import LoginRequestHandler
from routing.auth.response.logOutRequestHandler import LogOutRequestHandler
from service.dataBaseService import DataBaseService
from routing.route import Route
from const.pathConst import PathConst
from const.restConst import RestConst
from const.paramsConst import ParamsConst

class AuthRoute(Route):
    def __init__(self):
        self.__uuid = None
        self.__clientBD = DataBaseService.getInstance().clients

        super().__init__(None)

    # type is REST type
    def request(self, path, rest, params):
        response = super().request(path, rest, params)

        self.__updateLastVisit()

        return response

    def save(self):
        saveData = self.user.getChangeCompression()

        self.__clientBD.change(saveData)

    @property
    def getUUID(self):
        return self.__uuid

    def _routing(self):
        return {
                RestConst.GET: {
                    # PathConst.LOGIN             :   self.__login,
                    # PathConst.AUTHORIZATION     :   self.__registerGET
                    PathConst.AUTHORIZATION     :   self.__authGET
                },
                RestConst.POST:{
                    # PathConst.AUTHORIZATION     :   self.__registerPOST,
                    PathConst.LOGOUNT           :   self.__logOut    
                }
        }

    def __authGET(self, params):
        result = LoginRequestHandler()
        
        if ParamsConst.AUTHORIZATION in params:
            params = self.__authorizationCustomer(params[ParamsConst.AUTHORIZATION])

            if not params:
                result.setContentsUserNotExist()

                return result
    
        if not ParamsConst.UUID in params:
            params = self.__createClientParams()

        self.__setCurrentUser(params)            

        # if not validate uuid
        if not self.user:
            params = self.__createClientParams()

            self.__setCurrentUser(params)

        result.setContentsSuccess(self.user.GETResponse())

        return result

    def __createClientParams(self):
        insert = {}

        insert['uuid'] = str(uuid.uuid1())
        insert['createtime'] = str(time.time())
        insert['lastvisittime'] = str(time.time())

        self.__clientBD.insert(insert)

        return insert

    def __logOut(self, params):
        result = LogOutRequestHandler()

        if (isEqualFields(params, self.user)):
            result.setContentsSuccessfully()

            return result

        result.setContentsUserNotExist()

        return result

    def __setCurrentUser(self, params):
        if self.user: return 

        dbUser = self.__clientBD.read(params)
        
        self._Route__user = createObjectFromBD(CustomerVO, dbUser)

        if self.user:
            self.__uuid = self.user.uuid

    def __updateLastVisit(self):
        if self.user:
            self.user.lastvisittime = time.time()

    def __authorizationCustomer(self, authorization):
        profileBD = DataBaseService.getInstance().profile

        dbUser = profileBD.read(authorization)

        if dbUser and ParamsConst.UUID in dbUser:
            result = { ParamsConst.UUID:dbUser[ParamsConst.UUID] }

            return result

        return None
