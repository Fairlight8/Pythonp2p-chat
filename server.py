import socket
import select
import pickle

puertoserver=input("Introduzca el puerto:")     

listener = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

listener.bind(("localhost",int(puertoserver)))

listener.listen(5)

lista_peers=[]
lista_peers_proceso=[]      #cada peer es una tupla direccion,nombre, de los cuales la primera, la direccion tambien es uan tupla
lista_sockets=[listener]

while True:
    listos=select.select(lista_sockets,[],[])
    for s_descriptor in listos:
        if s_descriptor == listener:    #es una nueva conexion al socket
            nuevo_socket,nueva_dir = listener.accept()
            cadena = nuevo_socket.recv(32).decode()
            if cadena[:5] == "CONEX":   #alguien quiere entrar a la sala
                lista_sockets.append(socket.socket(socket.AF_INET,socket.SOCK_DGRAM))
            elif cadena[:5] == "LEAVE": #alguien quiere salir de la sala
            
            else:                           #no reconocemos el mensaje
            
        else:                           #es socket abierto de alguien que esta estableciendo conexion






