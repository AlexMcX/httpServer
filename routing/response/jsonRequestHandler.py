import json
from routing.response.requestHandler import RequestHandler

class JsonRequestHandler(RequestHandler):
    def getStatus(self):
        return 200

    def getContentType(self):
        return 'application/json'

    def getContents(self):
        return json.dumps(super().getContents())

    def setContentsBool(self, value):
        return super().setContents("{result:" + str(value) + "}")

