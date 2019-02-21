import time
import uuid
from utils.objectEx import *
from database.baseBase import DataBaseBase
from database.vo.userVO import UserVO
from response.loginRequestHandler import LoginRequestHandler
from response.registerRequestHandler import RegisterRequestHandler
from response.logOutRequestHandler import LogOutRequestHandler
class DataBaseUser(DataBaseBase):
    def __init__(self):
        self.__currentUser = None
        self.__uuid = None
        
        super().__init__(super().SQLITE3, 'db/userBD.db', 'users')

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

    # format insert bd - "uuid, email, password, createtime"
    def createUser(self, params):
        if (params):
            insert = params.copy()

            insert['uuid'] = str(uuid.uuid1())
            insert['time'] = time.time()

            isInsert = super().insert(insert)
            
            if (isInsert) :
                super().commit()

                return True

        return False

    def setCurrentUser(self, params):
        dbUser = super().readRow(params)
        
        self.__currentUser = createObjectFromBD(UserVO, dbUser)
        self.__uuid = self.__currentUser.uuid

    @property
    def getUUID(self):
        return self.__uuid