from database.vo.baseVO import BaseVO

class UserVO(BaseVO):   
    def __init__(self):
        self.email = None
        self.password = None
        self.firstName = None
        self.lastName = None
        self.nickName = None
        self.icon = None
        self.uuid = None
        self.createdate = None
        self.lastvisittime = None

    def _getUnique(self):
        return {'uuid':self.uuid}

    def getLoginResponse(self):
        params = [
            id(self.uuid),
            id(self.nickName),
            id(self.icon)
        ]

        return super()._createResponse(params)

    def getBaseEditResponse(self):
        params = [
            id(self.email),
            id(self.firstName),
            id(self.lastName),
            id(self.nickName),
            id(self.icon)
        ]

        return super()._createResponse(params)