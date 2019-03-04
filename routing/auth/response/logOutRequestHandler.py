import json
from routing.response.requestHandler import RequestHandler

class LogOutRequestHandler(RequestHandler):
    def getStatus(self):
        return 200

    def getContentType(self):
        return 'application/json'
    
    def setContentsUserNotExist(self):
        self.setContents({'result': False, 'message':'LogOut faild, user not exist'})

    def setContentsSuccessfully(self):
        self.setContents({'result': True})

    def getContents(self):
        return json.dumps(super().getContents())
