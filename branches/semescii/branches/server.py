# !-- coding: UTF-8 --!

import _my_ClientProccess

import socket


HOST = ''
PORT = 5007

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)

while 1:
    conn, addr = s.accept()
    _my_ClientProccess.ClientProccess(conn, addr).start()
