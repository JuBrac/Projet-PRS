import socket
import time
import os

def fragmentationFichier(contenu,nomFichier):


    tailleFichier = os.path.getsize(nomFichier)
    nbSegments = int(tailleFichier/1494)+1
    arrayFrame = []
    #contenu = '\n'.join(contenu)
    contenu = contenu.encode()
    for i in range(nbSegments):
        arrayFrame.append(contenu[i*1494:i*1494+1494])
    return arrayFrame

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
                        socket.bind(('0.0.0.0', 8787))
                        nomFichier = socket.recv(255)
                        nomFichier = nomFichier.decode("utf-8")
                        print(nomFichier[:nomFichier.find("\x00")])
                        nomFichier = nomFichier[:nomFichier.find("\x00")]
                        f = open(nomFichier, "r")
                        contenu = f.read()
                        listeMessage = fragmentationFichier(contenu,nomFichier)
                        t1 = time.perf_counter()
                        for i in range(len(listeMessage)):
                                numSequence = str(i+1)
                                while len(numSequence) < 6 :
                                        numSequence = "0"+numSequence
                                print(numSequence)
                                numSequence = numSequence.encode()
                                message = numSequence + listeMessage[i]
                                #print(message)
                                socket.sendto(message,address)
                        t2 = time.perf_counter()
                        t = (t2-t1)*10**3
                        tailleFichier = os.path.getsize(nomFichier)
                        débit = tailleFichier/t
                        print("Débit :", débit, "Kbytes/s")
                        continu = False




print ("Close")
socket.sendto(b'FIN',address)
serversocket.close()



# fragmentationFichier(contenu,nomFichier)
