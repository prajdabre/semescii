# !-- coding: UTF-8 --!
import _my_Client
import threading


HOST = "127.0.0.1"
PORT = 5007

client = _my_Client.Client(HOST, PORT)


p1 = threading.Thread(target=client.sendMyCoordinates, name="t1")
p2 = threading.Thread(target=client.getPlayersCoord, name="t2")
p1.start()
p2.start()