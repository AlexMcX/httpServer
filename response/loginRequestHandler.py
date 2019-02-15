import json
from response.requestHandler import RequestHandler

class LoginRequestHandler(RequestHandler):
    __contents = None

    def __init__(self):
        super().__init__()
        self.contentType = 'application/json'
        self.setStatus(200)

    def getContents(self):
        return self.__contents

    def setContentsUserNotExist(self):
        self.__contents = json.dumps({'result': False, 'message':'Email or password incorrect'})

    def setContentsSuccess(self, content):
        content['result'] = True

        self.__contents = json.dumps(content)

