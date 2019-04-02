from database.vo.baseVO import BaseVO
from const.restConst import RestConst 
class ProfileVO(BaseVO):
    def __init__(self):        
        self.email = None
        self.password = None
        self.firstName = None
        self.lastName = None
        self.userName = None
        self.icon = None

        super().__init__()
        

    def GETResponse(self):
        return self._createResponse(RestConst.GET, [id(self.uuid)])

    def GETResponseSub(self):
        return self._createResponse(RestConst.GET,[
                    id(self.uuid),
                    id(self.password)
                ])

    def GETResponseForm(self):
        result = self._createResponse(RestConst.GET, [id(self.uuid)], True)
        
        result['password'] = ""

        return result