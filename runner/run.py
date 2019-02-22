import servers

class Run:
    def __init__(self):
        self.server = None

        self.waitCommand()

    def waitCommand(self):
        while True:
            command = input('wait command:')            
            try:
                self.currentCommand[command]()
            except KeyError as e:
                print('Undefined command: {}'.format(e.args[0]))

            if (not self.server):
                return

    

    def startServer(self):
        if self.server:
            print('       - server exist, first need stop server, write \'stop\', in command line')
        self.server = servers.Servers()
        self.server.startServer()

    def stopServer(self):
        pass
        if self.server is None:
            print('       - server not create, please before create new Server')
            return

        self.server.stopServer()
        self.server = None

    @property
    def currentCommand(self):
        return {
            "start" : self.startServer,
            "stop"  : self.stopServer
        }
