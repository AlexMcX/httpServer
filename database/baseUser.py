import time
import uuid
from utils.objectEx import createObjectFromBD, parseToSqliteSelect, isEqualFields
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

        result.setContentsSuccess(self.__currentUser.uuid)

        return result

    def register(self, params):
        result = RegisterRequestHandler()

        if(self.isUser(params)):
            result.setContentsUserExist()

            return result
        
        # create new user if user not exist in base
        self.createUser(params[UserVO.EMAIL_CONST][0], params[UserVO.PASSWORD_CONST][0])

        result.setContentsSuccessfully()

        return result

    def logOut(self, params):
        result = LogOutRequestHandler()

        if (isEqualFields(params, self.__currentUser)):
            self.__currentUser = None

            result.setContentsSuccessfully()

            return result

        result.setContentsUserNotExist()

        return result

    def createUser(self, email, password):
        super().insert("'{}','{}','{}','{}'".format(uuid.uuid1(), email, password, time.time()))

        super().commit()

    def setCurrentUser(self, params):
        selected = parseToSqliteSelect(params)
        
        dbUser = super().readRow(selected)

        self.__currentUser = createObjectFromBD(UserVO, dbUser)