from database.vo.baseVO import BaseVO

class UserVO(BaseVO):
    email = None
    password = None
    firstName = None
    lastName = None
    nickName = None
    uuid = None
    createdate = None
    
    def __getResponses__(self):
        return [ 
                    id(self.email),
                    id(self.firstName),
                    id(self.lastName),
                    id(self.nickName),
                    id(self.uuid)
                ]