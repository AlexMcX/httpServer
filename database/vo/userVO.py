from database.vo.baseVO import BaseVO

class UserVO(BaseVO):   
    def __init__(self):
        self.email = None
        self.password = None
        self.firstName = None
        self.lastName = None
        self.nickName = None
        self.uuid = None
        self.createdate = None
        self.lastvisittime = None

    def _BaseVO__getResponses(self):
        return [ 
                    id(self.email),
                    id(self.firstName),
                    id(self.lastName),
                    id(self.nickName),
                    id(self.uuid)
                ]

    def _BaseVO__getUnique(self):
        return {'uuid':self.uuid}