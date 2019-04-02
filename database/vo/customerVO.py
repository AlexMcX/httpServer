from database.vo.baseVO import BaseVO
# from database.vo.profileVO import ProfileVO
# from const.restConst import RestConst

class CustomerVO(BaseVO):   
    def __init__(self):
        self.createtime = None
        self.lastvisittime = None
        self.type = None

        # ProfileVO
        self.profile = None

        super().__init__()

    
