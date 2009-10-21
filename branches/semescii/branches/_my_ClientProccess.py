# !-- coding: UTF-8 --!

import _my_DataProccess

import threading

class ClientProccess(threading.Thread):
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
                
        print "Connected by, ", self.addr
        threading.Thread.__init__(self)
    
    def run(self):
        while 1:
            data = self.conn.recv(1024)
            if not data: 
                break
            else :
                self._process_request(data)
                self.conn.send("hey")
        
        self.conn.close()
    
    def shot(self):
        print "Shot"
    
    def register(self, username, email, pswd):
        print "Register"
        
    def signin(self):
        print "Sign in"
        
    def _process_request(self, request):
        params = _my_DataProccess.DataProccess.decode(request)
        if params['action'] == 'register' : self.register(params['username'], params['email'], params['pswd'])
        else : print params;   