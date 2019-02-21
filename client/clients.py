from const.pathConst import PathConst
from client.client import Client
from response.badRequestHandler import BadRequestHandler

class Clients:
    def __init__(self):
        print(' <<<<<<<<<<<<<<< Create new clients instance >>>>>>>>>>>>>>>>> ')

        self.__clients = {}
        self.__cLoginID = None
        self.__cLogOutID = None

    def do_GET(self, path, params):
        client = self.__getClientToParams(params)

        if not client and path == PathConst.LOGIN:
            client = Client()           

            self.__listenersClient(client, True)

        if client:
            handler = client.do_GET(path, params)
        else:
            handler = BadRequestHandler()

        return handler

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
        self.__clients[client.UUID] = client

        print("    <<< LOGIN USER: total count:{}, user uuid:{} ".format(len(self.__clients), client.UUID))

    def __onLogout(self, client):
        if not client:
            return

        self.__listenersClient(client, False)
        self.__clients.pop(client.UUID, None)

        print("    <<< LOGOUT USER: total count:{}, user uuid:{}".format(len(self.__clients), client.UUID))
        
    # ***************************************************