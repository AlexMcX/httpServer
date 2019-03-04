import json
from routing.response.requestHandler import RequestHandler

class LoginRequestHandler(RequestHandler):    
    def getStatus(self):
        return 200

    def getContentType(self):
        return 'application/json'    

    def setContentsUserNotExist(self):
        self.setContents({'result': False, 'message':'Email or password incorrect'})

    def setContentsSuccess(self, content):
        content['result'] = True

        self.setContents(content)

    def getContents(self):
        return json.dumps(super().getContents())

