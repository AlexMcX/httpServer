import os
from const.pathConst import PathConst
from response.badRequestHandler import BadRequestHandler
from urllib.parse import parse_qs, urlparse, parse_qsl
from http.server import BaseHTTPRequestHandler
from client.client import Client

class Server(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.__clients = {}
        self.__cLoginID = None
        self.__cLogOutID = None
        print(' <<<<<<<<<<<<<<< Create new server instance >>>>>>>>>>>>>>>>> ')

        BaseHTTPRequestHandler.__init__(self, request, client_address, server)         

    @classmethod
    def pre_stop(cls):
        print ('Before calling Server close')
        # cls.dbUser.saveAndClose()

        # for uuid, client in cls.__clients.items():
        #     client.save()

        #     break

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

        client = self.__getClientToParams(params)

        if not client and path == PathConst.LOGIN:
            client = Client()           

            self.__listenersClient(client, True)

        if client:
            handler = client.do_GET(path, params)
        else:
            handler = BadRequestHandler()

        self.respond({
                'handler': handler
            })

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

    def __getClientToParams(self, params):
        uuid = None
        
        if 'uuid' in params:
            uuid = params['uuid'][0]

        if not uuid or not uuid in self.__clients:
            return None

        return self.__clients[uuid]

    # ******************** listeners ********************
    def __listenersClient(self, client, access):
        if not client:
            return

        if access:
            self.__cLoginID = client.onLogin.add((lambda client: self.__onLogin(client)))
            self.__cLogOutID = client.onLogout.add((lambda client: self.__onLogout(client)))
        else:
            client.onLogin.remove(self.__cLoginID)
            client.onLogout.remove(self.__cLogOutID)

    def __onLogin(self, client):
        print("\n LOGIN NEW USER: total count:{}, user uuid:{} \n".format(len(self.__clients), client.UUID))

        self.__clients[client.UUID] = client

    def __onLogout(self, client):
        if not client:
            return

        self.__listenersClient(client, False)
        self.__clients.pop(client.UUID, None)

        print("\n LOGOUT NEW USER: total count:{}, user uuid:{} \n".format(len(self.__clients), client.UUID))
        
    # ***************************************************
