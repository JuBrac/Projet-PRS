# coding: utf-8

from socket import *

hote = "localhost"
port = 2020
nomFichier = "input.txt"

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
socket.connect((hote, port))
print("Connection on {}".format(port))



continu=True

# while (continu==True):
socket.send(str.encode('SYN'))

synAck = socket.recv(255)
# print(str.decode(synAck))
if synAck.find(b'SYN-ACK')!=-1:
    print("SYN-ACK recue")
    portDataSocket = str(synAck[str(synAck).find('K')-1:])
    print(int(portDataSocket[2:len(portDataSocket)-1]))

    socket.send(str.encode('ACK'))

socket.connect((hote, 8787))
print("Connection on {}".format(port))

socket.send(str.encode(nomFichier))




continu=False

print("Close")
socket.close()
