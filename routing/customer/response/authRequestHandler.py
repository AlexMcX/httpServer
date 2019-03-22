import json
from routing.response.requestHandler import RequestHandler

class AuthRequestHandler(RequestHandler):    
    def getStatus(self):
        return 200

    def getContentType(self):
        return 'application/json'

    def setContentsUserExist(self):
        self.setContents({'result': False, 'message':'Register faild, user exist'})

    def setContentsSuccess(self, content = None):
        if not content:
            content = {} 

        content['result'] = True

        self.setContents(content)

    def getContents(self):
        return json.dumps(super().getContents())
