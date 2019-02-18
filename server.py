import os
from urllib.parse import parse_qs, urlparse, parse_qsl
from http.server import BaseHTTPRequestHandler
from routes.main import routes
from client.client import Client

class Server(BaseHTTPRequestHandler):
    __clients = {} 

    @classmethod
    def pre_stop(cls):
        print ('Before calling Server close')
        # cls.dbUser.saveAndClose()

        for uuid, client in cls.__clients.items():
            client.save()

            break

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
        isNewClient = False

        print('Server::do_GET - ', self.path)

        path = urlparse(self.path).path
        params = parse_qs(urlparse(self.path).query, keep_blank_values=False)

        if not 'uuid' in params:
            uuid = None
        else:
            uuid = params['uuid'][0]

        if not uuid or not uuid in self.__clients:
            client = Client()

            isNewClient = True
        else:
            print(params['uuid'][0])
            print(self.__clients)
            client = self.__clients[params['uuid'][0]]
        
        handler = client.do_GET(path, params)
        
        if isNewClient and client.getUUID():
            self.__clients[client.getUUID()] = client

            print("        APPEND NEW USER: uuid:", client.getUUID())

        self.respond({
                'handler': handler
            })       

    # промоніторити закриття сесії браузера і видатити слієнта якщо його немає
    # в браузері розібратись що відбувається коли закривається вкладка, як зробити щоб через х хв видалялись куки
    # закриття сесії в браузері

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
