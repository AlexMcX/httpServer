import os
import json
from urllib.parse import parse_qs, urlparse, parse_qsl
from http.server import BaseHTTPRequestHandler
from client.clients import Clients
from service.dataBaseService import DataBaseService

class Server(BaseHTTPRequestHandler):
    __clients = Clients()

    @classmethod
    def pre_stop(cls):
        print ('Before calling Server close')

        Server.__clients.save()

        DataBaseService.commitAndClose()

    @classmethod
    def after_stop(cls):
        print ('After calling Server close')

    def end_headers (self):
        self.send_header('Access-Control-Allow-Origin', '*')
        BaseHTTPRequestHandler.end_headers(self)

    def do_HEAD(self):
        pass

    def do_OPTIONS(self):
        origin = self.headers.get('origin')
        
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", origin)
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")

    def do_GET(self):
        print('Server::do_GET - ', self.path)

        if 'Content-Length' in self.headers:
            content_length = int(self.headers['Content-Length'])
            params = self.rfile.read(content_length)
        else:
            params = parse_qs(urlparse(self.path).query, keep_blank_values=False)
        
        if params:
            self.__request(params)

    def do_POST(self):
        print('Server:do_POST --- ', self.path)

        content_length = int(self.headers['Content-Length'])
        params = self.rfile.read(content_length)
        
        self.__request(params)

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

    def __request(self, strValue):
        path = urlparse(self.path).path

        if isinstance(strValue, dict):
            params = strValue
        else:
            params = json.loads(strValue)

        self.respond({
                'handler': Server.__clients.request(path, params)
            })
