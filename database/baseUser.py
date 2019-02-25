import time
import uuid
from utils.objectEx import *
from database.baseBase import DataBaseBase
from database.vo.userVO import UserVO
from response.loginRequestHandler import LoginRequestHandler
from response.registerRequestHandler import RegisterRequestHandler
from response.logOutRequestHandler import LogOutRequestHandler
from service.dataBaseService import DataBaseService
class DataBaseUser(DataBaseBase):
    def __init__(self):
        self.__currentUser = None
        self.__uuid = None
        self.__userBD = DataBaseService.getInstance().users

    def login(self, params):
        result = LoginRequestHandler()

        self.setCurrentUser(params)

        if(not self.__currentUser):
            result.setContentsUserNotExist()

            return result

        result.setContentsSuccess(self.__currentUser.getResponse())

        return result

    def register(self, params):
        result = RegisterRequestHandler()

        result.setContentsUserExist()

        if(self.__currentUser):
            return result
        
        # create new user if user not exist in base
        isCreateUser = self.createUser(params)
        
        if (isCreateUser):
            self.setCurrentUser(params)

            result.setContentsSuccess(self.__currentUser.getResponse())           

        return result

    def logOut(self, params):
        result = LogOutRequestHandler()

        if (isEqualFields(params, self.__currentUser)):
            self.__currentUser = None

            result.setContentsSuccessfully()

            return result

        result.setContentsUserNotExist()

        return result

    def save(self):
        saveData = self.__currentUser.getChangeCampression()

        self.__userBD.change(saveData)

    # format insert bd - "uuid, email, password, createtime"
    def createUser(self, params):
        if (params):
            insert = params.copy()

            insert['uuid'] = str(uuid.uuid1())
            insert['time'] = time.gmtime()
            insert['lastvisittime'] = time.time()

            isInsert = self.__userBD.insert(insert)
            
            if (isInsert) :
                self.__userBD.commit()

                return True

        return False

    def setCurrentUser(self, params):
        dbUser = self.__userBD.read(params)
        
        self.__currentUser = createObjectFromBD(UserVO, dbUser)
        
        if self.__currentUser:
            self.__uuid = self.__currentUser.uuid

    def updateLastVisit(self):
        if self.__currentUser:
            self.__currentUser.lastvisittime = time.time()

    @property
    def getUUID(self):
        return self.__uuid