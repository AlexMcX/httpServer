from database.vo.baseVO import BaseVO

class UserVO(BaseVO):
    uuid = None
    email = None
    password = None
    firstName = None
    lastName = None
    nickName = None
    createdate = None
    
    def __getResponses__(self):
        return [
                    id(self.uuid), 
                    id(self.email),
                    id(self.firstName),
                    id(self.lastName),
                    id(self.nickName)
                ]