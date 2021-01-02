import socket
import select
from datetime import datetime
import os

def lectureFichier(nomFichier):
    nomFichier = nomFichier.decode("utf-8")
    nomFichier = nomFichier[:nomFichier.find("\x00")]
    f = open(nomFichier, "r")
    contenu = f.read()
    return contenu,nomFichier
def fragmentationFichier(contenu,nomFichier):



    tailleFichier = os.path.getsize(nomFichier)
    nbSegments = int(tailleFichier/1494)+1
    arrayFrame = []

    for i in range(nbSegments):
        arrayFrame.append(contenu[i*1494:i*1494+1494])
    return arrayFrame

def numeroSequenceByte(index):
    numSequence = str(index+1)
    while len(numSequence) < 6 :
        numSequence = "0"+numSequence
    numSequenceByte = numSequence.encode("utf-8")
    return numSequenceByte




# create an INET, STREAMing socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# bind the socket to a public host, and a well-known port
serversocket.bind(('0.0.0.0', 2020))
# become a server socket

continu=True

while (continu==True):
        syn, address = serversocket.recvfrom(len("SYN"))
        # print(syn)
        if syn == b'SYN':
                print ("SYN recu")
                # t1 = time.perf_counter()
                t1 = datetime.now()
                serversocket.sendto(b'SYN-ACK8787',address)
                ack = serversocket.recv(len("ACK"))
                if ack == b'ACK':
                        t2 = datetime.now()
                        print("ACK recu")
                        rtt = (t2-t1)
                        rtt = rtt.microseconds
                        print("RTT = ",rtt, "us")
                        socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        socket.bind(('0.0.0.0', 8787))
                        nomFichier = socket.recv(255)
                        contenu,nomFichier = lectureFichier(nomFichier)
                        listeMessage = fragmentationFichier(contenu,nomFichier)
                        swnd = 16
                        rto = rtt*5*10**-6
                        numDernierAck = 0
                        i=0
                        while(i<len(listeMessage)): # Tant qu'on n'a pas envoye tout les messages.
                            for j in range(swnd):
                                message = numeroSequenceByte(j) + listeMessage[j]
                                socket.sendto(message,address)
                                # print("SWND:",swnd,i)
                                # print("Num sequence envoye:",numSequence)
                            i = i+swnd-1
                            # print("i: ",i)

                            ackRecu=0
                            pertePaquet = 0
                            while(numDernierAck!=len(listeMessage)): # Tant que le numero du dernier acquittement n'est pas celui du dernier message.
                                # print("boucle")
                                inputs = [socket]
                                read,write,error = select.select(inputs,[],[],rto)
                                for s in read: # Si une socket est dispo en lecture.
                                    if s is socket:
                                        data = s.recv(255)
                                        print(data)
                                        # if len(data)!=0:
                                        data=data.decode()
                                        data = data[:data.find('\x00')]
                                        if(int(data[3:])>numDernierAck):
                                            numDernierAck = int(data[3:])
                                            print("ACK "+str(numDernierAck)+" recue")
                                            i = numDernierAck
                                            if(i<len(listeMessage)):
                                                message = numeroSequenceByte(i) + listeMessage[i]
                                                socket.sendto(message,address)



                                if(len(read)==0):
                                    print("====== Perte de paquet ======")
                                    # socket.sendto(message,address)                                  
                                    pertePaquet = 1
                                    i = numDernierAck
                                    if(i<len(listeMessage)):
                                        message = numeroSequenceByte(i) + listeMessage[i]
                                        socket.sendto(message,address)



                        socket.sendto(b'FIN',address)
                        continu = False




print ("Close")
t2 = datetime.now()
tempsTotal = (t2 - t1)
tailleFichier = os.path.getsize(nomFichier)
print(tailleFichier)
print(tempsTotal.seconds,tempsTotal.microseconds)
tempsTotal = tempsTotal.seconds + tempsTotal.microseconds*10**-6
print(tempsTotal)
print((tailleFichier/tempsTotal)*10**-3,"Ko/s")
serversocket.close()



# fragmentationFichier(contenu,nomFichier)
