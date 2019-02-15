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

    __getPath__ = {
            '/login'    :   dbUser.login,
            '/auth'     :   dbUser.register,
            '/logout'   :   dbUser.logOut
        }

    @classmethod
    def pre_stop(cls):
        print ('Before calling Server close')
        cls.dbUser.saveAndClose()

    @classmethod
    def after_stop(cls):
        print ('After calling Server close')

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

        call = self.__getPath__.get(path)

        if (call):
            handler = call(params)
        else:
            handler = BadRequestHandler()

            print('Undefined client command: {}'.format(path))

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
