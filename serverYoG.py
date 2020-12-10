import socket
import time

# create an INET, STREAMing socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# bind the socket to a public host, and a well-known port
serversocket.bind(('0.0.0.0', 2020))
# become a server socket

continu=True

while (continu==True):
        syn, address = serversocket.recvfrom(len("SYN"))
        print(syn)
        if syn == b'SYN':
                print ("SYN reçu")
                t1 = time.perf_counter()
                serversocket.sendto(b'SYN-ACK8787',address)
                ack = serversocket.recv(len("ACK"))
                if ack == b'ACK':
                        t2 = time.perf_counter()
                        print("ACK reçu")
                        rtt = (t2-t1)*10**6
                        print("RTT = ",rtt, "us")
                        socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        socket.bind(('localhost', 8787))
                        nomFichier = socket.recv(255)
                        f = open(nomFichier, "r")
                        contenu = f.readlines()
                        NbSegments = len(contenu)
                        for i in range(NbSegments):
                                NumSequence = str(i)
                                while len(NumSequence) < 6 :
                                        NumSequence = "0"+NumSequence
                                message = NumSequence + contenu[i]
                                socket.sendto(message,address)
                        continu = False




print ("Close")
serversocket.close()
