import servers
import threading

class Run:
    thread = None
    server = None

    def __init__(self):
        self.thread = threading.Thread(None, self.waitCommand)
        self.thread.start()

    def waitCommand(self):
        while True:
            command = input('wait command:')

            try:
                self.runCurrentCommand()[command]()
            except KeyError as e:
                print('Undefined command: {}'.format(e.args[0]))

            if (not self.thread):
                return


    def runCurrentCommand(self):
        return {
            "exit"  : self.exit,
            "start" : self.startServer,
            "stop"  : self.stopServer
        }

    def startServer(self):
        self.server = servers.Servers()
        self.server.startServer()

    def stopServer(self):
        if self.server is None:
            print('       - server not create, please before create new Server')
            return

        self.server.stopServer()
        self.server = None

    def exit(self):
        self.thread.should_abort_immediately = True
        self.thread = None
