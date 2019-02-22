import time
from http.server import HTTPServer
from server import Server
import threading
from importlib import reload
from database.baseUser import DataBaseUser

class Servers():    
    HOST_NAME = 'localhost'
    PORT_NUMBER = 4201   

    def __init__(self):
        print('<<<<<<<<<<<<<<< Create new servers instance >>>>>>>>>>>>>>>>>')
        self.thread = None

        self.httpd = HTTPServer((Servers.HOST_NAME, Servers.PORT_NUMBER), Server)

    def startServer(self): 
        if self.thread:
            print('Error: need stop server, wite stop to conslole')     
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

        pass


