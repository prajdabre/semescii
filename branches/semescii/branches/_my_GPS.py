# !-- coding: UTF-8 --!
import random
class GPS:
    def __init__(self):
        print "class GPS inited"
    
    #возращаем текущее местоположение пользователя
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
    