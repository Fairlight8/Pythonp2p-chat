import socket
import select
import pickle

def actualizarlistaalospeers(lista):
    for peer in lista_peers:
        s_descriptor.sendto(pickle.dumps(lista_peers), peer[1])


if __name__ == "__main__":

    puertoserver=input("Introduzca el puerto:")

    listener = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    listener.bind(("localhost",int(puertoserver)))

    listener.listen(5)

    lista_peers=[]          #cada peer es una tupla de nombre y direccion, la cual tambien es una tupla
    lista_sockets=[listener]

    while True:
        listos=select.select(lista_sockets,[],[])
        for s_descriptor in listos[0]:
            print("Entrado en el for")
            print(s_descriptor)
            print(listener)
            if s_descriptor == listener:    #es una nueva conexion al socket
                print("Es el listener")
                nuevo_socket,nueva_dir = listener.accept()
                cadena = nuevo_socket.recv(32).decode()
                print("Ha recibido algo"+cadena)
                if cadena[:5] == "CONEX":   #alguien quiere entrar a la sala
                    print("Ha entrado en el conex")
                    nuevo_socket_udp=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                    nuevo_socket_udp.sendto("NAME".encode(),(nueva_dir[0],int(cadena[6:])))
                    print("He mandado la cadena a ")
                    print((nueva_dir[0],int(cadena[6:])))
                    lista_sockets.append(nuevo_socket_udp)
                elif cadena[:5] == "LEAVE": #alguien quiere salir de la sala
                    print("Ha entrado en el leave")
                    puerto_desconexion=int(cadena[6:])
                    for peer in lista_peers:
                        if peer[1][1] == puerto_desconexion:
                            lista_peers.remove(peer)
                            for peer in lista_peers:
                                socket.socket(socket.AF_INET,socket.SOCK_DGRAM).sendto(pickle.dumps(lista_peers), peer[1])  #creo un socket udp solo para mandarlo

                else:                           #no reconocemos el mensaje
                    print("QUEEEESESTOLOCO")
            else:                           #es socket abierto UDP de alguien que esta estableciendo conexion
                print("Ha entrado en el else")
                recibo_udp=s_descriptor.recvfrom(32)
                lista_peers.append((recibo_udp[0].decode(),recibo_udp[1]))  #añadimos a la lista le nuevo peer
                for peer in lista_peers:
                    s_descriptor.sendto(pickle.dumps(lista_peers),peer[1])





