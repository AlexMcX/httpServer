from routing.response.requestHandler import RequestHandler

class BadRequestHandler(RequestHandler):
    def getStatus(self):
        return 400

    def getContentType(self):
        return 'text/plain'