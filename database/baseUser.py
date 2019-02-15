import time
import uuid
from utils.objectEx import *
from database.baseBase import DataBaseBase
from database.vo.userVO import UserVO
from response.loginRequestHandler import LoginRequestHandler
from response.registerRequestHandler import RegisterRequestHandler
from response.logOutRequestHandler import LogOutRequestHandler

class DataBaseUser(DataBaseBase):   

    __UUID = None
    __currentUser = None

    def __init__(self):
        super().__init__('db/userBD.db', 'users')

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
        insert = prsetoSqliteInsert(params)

        print('      - ', insert)

        if (insert):
            insert = "'{}',{},'{}'".format(uuid.uuid1(), insert, time.time())

            isInsert = super().insert(insert)

            if (isInsert) :
                super().commit()

                return True

        return False

    def setCurrentUser(self, params):
        selected = parseToSqliteSelect(params)

        dbUser = super().readRow(selected)
        
        self.__currentUser = createObjectFromBD(UserVO, dbUser)