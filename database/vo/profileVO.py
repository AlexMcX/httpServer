from database.vo.baseVO import BaseVO
from const.restConst import RestConst 

class ProfileVO(BaseVO):
    def __init__(self):
        self.email = None
        self.password = None
        self.firstName = None
        self.lastName = None
        self.nickName = None
        self.icon = None

        super().__init__()

    def GETResponse(self):
        return self._createResponse(RestConst.GET, [id(super.uuid)])