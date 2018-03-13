import socket

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

s.sendto("holaaa".encode(),("127.0.0.1",5000))

s.close()