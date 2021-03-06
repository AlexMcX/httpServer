import json
import base64
from urllib.parse import parse_qs, urlparse, parse_qsl
from http.server import BaseHTTPRequestHandler
from users.customers import Customers
from service.dataBaseService import DataBaseService
from const.restConst import RestConst
from const.paramsConst import ParamsConst

class Server(BaseHTTPRequestHandler):
    __customers = Customers()

    @classmethod
    def pre_stop(cls):
        print ('Before calling Server close')

        Server.__customers.save()

        DataBaseService.commitAndClose()

    @classmethod
    def after_stop(cls):
        print ('After calling Server close')

    def end_headers (self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        BaseHTTPRequestHandler.end_headers(self)

    def do_HEAD(self):
        pass

    # def do_OPTIONS(self):
        # origin = self.headers.get('origin')
        
        # self.send_response(200)
        # self.send_header("Access-Control-Allow-Origin", origin)
        # self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        # self.send_header("Access-Control-Allow-Headers", "X-Requested-With")

    def do_GET(self):
        print('Server::do_GET - headers \n', self.headers)


        if 'Content-Length' in self.headers:
            content_length = int(self.headers['Content-Length'])

            params = self.rfile.read(content_length)
        else:
            params = parse_qs(urlparse(self.path).query, keep_blank_values=False)

        print('Server::do_GET - ', self.path, " | ")

        self.__parseAuthorization(params)

        self.__request(params, RestConst.GET)

    def do_POST(self):
        print('Server::do_POST - headers \n', self.headers)

        content_length = int(self.headers['Content-Length'])
        params = self.rfile.read(content_length)

        print('Server::do_POST - ', self.path, " | ", params)

        self.__request(params, RestConst.POST)

    def handle_http(self, handler):
        status_code = handler.getStatus()

        self.send_response(status_code)

        if status_code is 200:
            content = handler.getContents()
            self.send_header('Content-type', handler.getContentType())
        else:
            content = "404 Not Found"

        self.end_headers()
        
        return bytes(content, 'UTF-8')

    def respond(self, opts):
        response = self.handle_http(opts['handler'])
        self.wfile.write(response)

    def __request(self, strValue, rest):
        path = urlparse(self.path).path

        if isinstance(strValue, dict):
            params = strValue
        else:
            params = json.loads(strValue)

        self.respond({
                'handler': Server.__customers.request(path, rest, params)
            })

    def __parseAuthorization(self, params):
        if not ParamsConst.AUTHORIZATION in self.headers:
            return

        authorization = self.headers[ParamsConst.AUTHORIZATION]        
        authmeth, auth = authorization.split(' ')

        params[ParamsConst.AUTHORIZATION] = {}

        if authmeth.lower() == 'basic':
            auth = base64.b64decode(auth).decode('utf-8')
            username, password = auth.split(':')

            if '@' in username:
                params[ParamsConst.AUTHORIZATION][ParamsConst.EMAIL] = username
            
            params[ParamsConst.AUTHORIZATION][ParamsConst.PASSWORD] = password