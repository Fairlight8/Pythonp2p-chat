import select
import socket
import pickle
import sys

comandos_server = ["NEW"]

puertoserver=input("Introduzca el puerto del servidor:")

ipserver=input("Introduzca la direccion IP del servidor:")

tupla_server = ipserver,int(puertoserver)

socket_envio = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
listener_chat = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

listener_chat.bind(("localhost",0))

socket_envio.sendto((str)(listener_chat.getsockname()[1]).encode(),tupla_server)

listapickle,tupla_server=socket_envio.recvfrom(1024)

lista_peers=pickle.loads(listapickle)

set_sd = [sys.stdin,listener_chat]

while True:
    listos=select.select(set_sd,[],[])
    for i in listos[0]:
        if i is sys.stdin:     #es nuestro teclado
            cadena=input()
            for j in lista_peers:
                listener_chat.sendto(cadena.encode(),j)

        if i is listener_chat:                                   #es un mensaje entrante
            cadena,tuplapeer=listener_chat.recvfrom(1024)
            cadena=cadena.decode()
            if tuplapeer not in lista_peers:    #mensaje entrante de alguien no en el server
                if tuplapeer == tupla_server:   #es información del propio server
                    if cadena in comandos_server:    #es un mensaje del server
                        new,tuplapeer=listener_chat.recvfrom(1024)
                        lista_peers.append(pickle.loads(new))
                    else:                               #hemos recibido algo que no esperabamos
                        print("Error en recepcion del server")
                else:                           #es informacion de alguien que ni es el server ni un peer registrado
                    print("Hemos recibido una cadena de alguien no registrado")
                    print(lista_peers)
                    print(tuplapeer)
                    
            else:
                print("He recibido esta cadena")                               #mensaje registrado
                print(cadena)




