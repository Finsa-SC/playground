import socket

addr = ("192.168.1.1", 443)

s = socket.socket()
s.connect(addr)
s.close()