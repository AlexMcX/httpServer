from database.vo.baseVO import BaseVO

if __name__ == '__main__':
    cl = UserVO()
    print(cl.getAll())

class UserVO(BaseVO):
    uuid = None
    email = None
    password = None
    createdate = None

    def getAll(self):
        return (self.uuid, self.email)