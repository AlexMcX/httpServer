import os
from urllib.parse import parse_qs, urlparse, parse_qsl
from http.server import BaseHTTPRequestHandler
from routes.main import routes
from database.baseUser import DataBaseUser
from response.staticHandler import StaticHandler
from response.templateHandler import TemplateHandler
from response.badRequestHandler import BadRequestHandler

class Server(BaseHTTPRequestHandler):
    dbUser = DataBaseUser()

    @classmethod
    def pre_stop(cls):
        print ('Before calling Server close')
        cls.dbUser.saveAndClose()


    def end_headers (self):
        self.send_header('Access-Control-Allow-Origin', '*')
        BaseHTTPRequestHandler.end_headers(self)

    def do_HEAD(self):
        return

    def do_POST(self):
        print('Server:do_POST --- ')

    def do_GET(self):
        print('Server::do_GET - ', self.path)

        path = urlparse(self.path).path
        params = parse_qs(urlparse(self.path).query, keep_blank_values=False)

        try:
            handler = self.getGetHandlers()[path](params)          
        except KeyError as e:
            handler = BadRequestHandler()

            print('Undefined client command: {}'.format(e.args[0]))

        self.respond({
                'handler': handler
            })       

    def handle_http(self, handler):
        print('Server::handle_http - ')
        status_code = handler.getStatus()

        self.send_response(status_code)

        if status_code is 200:
            content = handler.getContents()
            self.send_header('Content-type', handler.getContentType())
        else:
            content = "404 Not Found"

        self.end_headers()
        print('handle_http content: ', content)
        return bytes(content, 'UTF-8')

    def respond(self, opts):
        response = self.handle_http(opts['handler'])
        self.wfile.write(response)

    def getGetHandlers(self):
        return {
            "/login"    :   self.dbUser.login,
            "/auth"     :   self.dbUser.register,
            "/logout"   :   self.dbUser.logOut
        }

    # def getGetHandler(self, path, params):
    #     return {
    #         path == '/login': self.dbUser.login(params['username'][0], params['password'][0]),
    #         path == '/auth':  self.dbUser.register(params['username'][0], params['password'][0]),
    #         path == path :BadRequestHandler()
    #     }[True]
