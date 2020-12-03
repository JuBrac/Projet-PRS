import socket

# create an INET, STREAMing socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# bind the socket to a public host, and a well-known port
serversocket.bind(('localhost', 2020))
# become a server socket

portSocketData = 8787

continu=True

# while (continu==True):

        # serversocket.listen(5)
        # client, address = serversocket.accept()
        # print ("{} connected".format( address ))

syn,adress = serversocket.recvfrom(255)
# print(syn)
connexionEtablie = False
if syn == b'SYN':
    print ("SYN recue")
    serversocket.sendto(b'SYN-ACK8787',adress)
    ack=serversocket.recv(255)
    if (ack==b'ACK'):
        print('ACK recue')
        connexionEtablie = True
if connexionEtablie == True:
    dataSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dataSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # bind the socket to a public host, and a well-known port
    dataSocket.bind(('localhost', portSocketData))

    nomFichier = dataSocket.recv(255)
    print(nomFichier)


    continu = False



print ("Close")
serversocket.close()
