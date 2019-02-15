import time
from http.server import HTTPServer
from server import Server
import threading
from importlib import reload
from database.baseUser import DataBaseUser

class Servers():
    
    HOST_NAME = 'localhost'
    PORT_NUMBER = 4201
    HOT_KEY_START_SERVER = 'ctrl+s'
    HOT_KEY_STOP_SERVER = 'ctrl+q'
    HOT_KEY_RESET_SERVER = 'ctrl+r'

    httpd = None
    thread = None

    def __init__(self):
        print('Servers init')
        self.httpd = HTTPServer((self.HOST_NAME, self.PORT_NUMBER), Server)

    def startServer(self): 
        if self.thread is not None:
            print('Error: need stop server, press {} or {}'.format(self.HOT_KEY_STOP_SERVER, self.HOT_KEY_RESET_SERVER))     
            return
        print(time.asctime(), 'Server Starts - %s:%s' % (self.HOST_NAME, self.PORT_NUMBER))
        self.thread = threading.Thread(None, self.httpd.serve_forever)
        self.thread.start()

    def stopServer(self):
        print(time.asctime(), 'Server Stops - %s:%s' % (self.HOST_NAME, self.PORT_NUMBER))
        self.httpd.RequestHandlerClass.pre_stop()
        self.httpd.shutdown()
        self.thread.join()
        self.httpd.RequestHandlerClass.after_stop()
        self.thread = None
        self.httpd = None

    def reload(self, httpd):
        if self.thread is not None and self.thread.isAlive:
            self.stopServer()
        
        self.startServer()


