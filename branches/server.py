# !-- coding: UTF-8 --!

import socket
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
                print data;
                self.conn.send("hey")
        
        self.conn.close()
    
    def shot(self):
        print "Shot"
    
    def register(self):
        print "Register"
        
    def signin(self):
        print "Sign in"

HOST = ''
PORT = 5007

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)

while 1:
    conn, addr = s.accept()
    ClientProccess(conn, addr).start()
