from const.pathConst import PathConst
from users.customer import Customer
from routing.response.badRequestHandler import BadRequestHandler
from const.restConst import RestConst

class Customers:
    def __init__(self):
        print(' <<<<<<<<<<<<<<< Create new clients instance >>>>>>>>>>>>>>>>> ')

        self.__clients = {}
        self.__cLoginID = None
        self.__cLogOutID = None

    def request(self, path, rest, params):
        handler = None

        customer = self.__getClientToParams(params)
        
        if not customer and path == PathConst.AUTHORIZATION:
            if rest == RestConst.GET:
                customer = Customer()           
            
                self.__listenersClient(customer, True)

        if customer:
            handler = customer.request(path, rest, params)

        if not handler:
            handler = BadRequestHandler()

        return handler

    def save(self):
        for uuid, client in self.__clients.items():
            client.save()

    def __getClientToParams(self, params):
        uuid = None
        
        if 'uuid' in params:
            if isinstance(params['uuid'], list):
                uuid = params['uuid'][0]
            else:
                uuid = params['uuid']

        if not uuid or not uuid in self.__clients:
            return None

        return self.__clients[uuid]

    # def __createClient(self, params):
    #     if 'type' in params:
    #         if params['type'] == 'guest':
    #             return Guest()

    #     return None
        

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

    def __onLogin(self, customer):
        if customer.UUID:
            self.__clients[customer.UUID] = customer

            print("    <<< LOGIN USER: total count:{}, user uuid:{} ".format(len(self.__clients), customer.UUID))
        else:
            self.__listenersClient(customer, False)

            customer.dispose()

            del customer

            print("    <<< FAILD LOGIN USER")

    def __onLogout(self, customer):
        if not customer:
            return

        self.__listenersClient(customer, False)
        self.__clients.pop(customer.UUID, None)

        customer.dispose()       

        print("    <<< LOGOUT USER: total count:{}, user uuid:{}".format(len(self.__clients), customer.UUID))

        del customer
    # ***************************************************