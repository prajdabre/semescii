# !-- coding: UTF-8 --!
import random
class GPS:
    def __init__(self):
        print "class GPS inited"
    
    #пока что в виде заглушки
    def getPos(self):
        try:
            self.lon
            self.lat 
        except:
            self.lon = float(67.0545)
            self.lat = float(73.0435)
            
        self.lon = self.lon + float(random.randrange(0, 2)) / 100
        self.lat = self.lat + float(random.randrange(0, 2)) / 100
        return {"lon":self.lon, "lat":self.lat}
    

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
                self.gps = GPS()
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
        
            
            


import threading



HOST = "127.0.0.1"
PORT = 5007


client = Client(HOST, PORT)


p1 = threading.Thread(target=client.sendMyCoordinates, name="t1")
p2 = threading.Thread(target=client.getPlayersCoord, name="t2")
p1.start()
p2.start()