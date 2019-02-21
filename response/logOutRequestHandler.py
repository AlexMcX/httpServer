import json
from response.requestHandler import RequestHandler

class LogOutRequestHandler(RequestHandler):
    def __init__(self):
        super().__init__()
        self.__contents = None
        self.contentType = 'application/json'
        self.setStatus(200)

    def getContents(self):
        return self.__contents

    def setContents(self, value):
        self.__contents = value
    
    def setContentsUserNotExist(self):
        self.__contents = json.dumps({'result': False, 'message':'LogOut faild, user not exist'})

    def setContentsSuccessfully(self):
        self.__contents = json.dumps({'result': True})