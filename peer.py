import select
import socket
import pickle
import sys


puertoserver=input("Introduzca el puerto del servidor:")

ipserver=input("Introduzca la direccion IP del servidor:")



tupla_server = ipserver,int(puertoserver)

socket_server = socket.socket() #ES TCP
listener_chat = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #ES UDP

listener_chat.bind(("localhost",0))

socket_server.connect(tupla_server)
socket_server.sendall(("CONEX "+str(listener_chat.getsockname()[1])).encode())


cadena,tupla_server=listener_chat.recvfrom(32)

lista_peers=[]

if cadena.decode() == "NAME" and tupla_server[0] == socket_server.getpeername()[0]:
    listener_chat.sendto(input("Introduzca nombre: ").encode(),tupla_server)
    listapickle,tupla_server=listener_chat.recvfrom(1024)
    lista_peers=pickle.loads(listapickle)
    socket_server.close()

else:
    print("No nos ha respondido el server")
    sys.exit(-1)

print(lista_peers)


set_sd = [sys.stdin,listener_chat]
try:
    while True:
        listos=select.select(set_sd,[],[])
        for i in listos[0]:
            if i is sys.stdin:     #es nuestro teclado
                cadena=input()
                for peer in lista_peers:
                    if peer[1] != listener_chat.getsockname():
                        listener_chat.sendto(cadena.encode(), peer[1])

            if i is listener_chat:                                   #es un mensaje entrante
                recib,dir_peer=listener_chat.recvfrom(1024)
                print("DIr peer ahora es")
                print(dir_peer)
                flag_server = True
                for peer in lista_peers:
                    if dir_peer == peer[1]:  # hemos encontrado el peer que nos lo ha mandado
                        print("\t\t\t" + peer[0] + " : " + recib.decode())
                        flag_server=False
                        break
                if flag_server == True:
                    print("Hemos recibido una lista del server")
                    lista_peers_temp = pickle.loads(recib)
                    if len(lista_peers_temp) > len(lista_peers):
                        print(lista_peers_temp[-1][0] + " se ha unido a la sala")
                    else:
                        flag=True
                        for k in range(len(lista_peers_temp)):
                            print(lista_peers_temp[k])
                            print(lista_peers[k])
                            if lista_peers_temp[k] != lista_peers[k]: #Si encontramso una diferencia recorriendo es que se ha ido alguien
                                print(lista_peers[k][0] + " ha abandonado la sala")
                                break
                                flag=False
                        if flag:
                            print(lista_peers[-1][0] + " ha abandonado la sala")
                    lista_peers=lista_peers_temp

except KeyboardInterrupt:

    tupla_server = ipserver, int(puertoserver)

    socket_server = socket.socket()  # ES TCP
    socket_server.connect(tupla_server)
    socket_server.send(("LEAVE " + str(listener_chat.getsockname()[1])).encode())
    print("Hasta luego :)")
    sys.exit(0)















