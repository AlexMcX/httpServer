import json
from response.requestHandler import RequestHandler

class RegisterRequestHandler(RequestHandler):
    __contents = None

    def __init__(self):
        super().__init__()
        self.contentType = 'application/json'
        self.setStatus(200)

    def getContents(self):
        return self.__contents 
        
        # json.dumps({'result': False, 'message':'Register succesfull'})

    def setContents(self, value):
        self.__contents = value
    
    def setContentsUserExist(self):
        self.__contents = json.dumps({'result': False, 'message':'Register faild, user exist'})

    def setContentsSuccess(self, content):
        content['result'] = True

        self.__contents = json.dumps(content)