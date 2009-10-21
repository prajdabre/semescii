# !-- coding: UTF-8 --!
import _my_GPS
import socket
import time
class Client:
    def __init__(self, host, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))
        print "class Client inited"
    
    def signin(self):
        print "Authorization complete"
        
    def shot(self):
        self.s.send("Shot")
        data = self.s.recv(1024)
        print "Received:", repr(data)
        print "Shot!"
        
    def disconnect(self):
        self.s.close()
        print "Connection closed"
        
    def register(self, username, email, pswd):
        regmsg = """username:%s;email:%s;pswd:%s""" % (username, email, pswd)
        self.s.send(regmsg)
        print "You registered"
    
    def sendMyCoordinates(self):
        while 1:
            time.sleep(1)
          
            #инициализируем gps, если еще не инициализирован
            try:
                self.gps
            except:
                self.gps = _my_GPS.GPS()
                self.pos = {"lon":0, "lat":0}
                
                
            #получаем координаты
            pos = self.gps.getPos()
            
            #отправляем координаты если они изменились
            if pos["lon"] != self.pos["lon"] and pos["lat"] != self.pos["lat"]:
                self.pos = pos
                msg = """Sending %s, %s""" % (self.pos["lon"], self.pos["lat"])
                self.s.send(msg)
           
    def getPlayersCoord(self):
        while 1:
            data = self.s.recv(1024)
            print "Received: ", data  