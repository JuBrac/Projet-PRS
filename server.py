import socket
import select
from datetime import datetime
import os
from math import floor
import sys

def lectureFichier(nomFichier):
    nomFichier = nomFichier.decode("utf-8")
    nomFichier = nomFichier[:nomFichier.find("\x00")]
    print(nomFichier)
    tailleFichier = os.path.getsize(nomFichier)
    f = open(nomFichier, "r")
   # f.seek(cursor1)
    contenu = f.read()
    f.close()
    return contenu,tailleFichier
    
def fragmentationFichier(contenu,tailleFichier):
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


portServeur = int(sys.argv[1])

# create an INET, STREAMing socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# bind the socket to a public host, and a well-known port
serversocket.bind(('0.0.0.0', 2020))
# become a server socket

continu=True
nbPaquetsCache = 50

while (continu==True):
        syn, address = serversocket.recvfrom(len("SYN"))
        if syn == b'SYN':
                print ("SYN recu")
                t1 = datetime.now()
                serversocket.sendto(b'SYN-ACK8787',address)
                ack = serversocket.recv(len("ACK"))
                if ack == b'ACK':
                    t2 = datetime.now()
                    print("ACK recu")
                    rtt = (t2-t1)
                    rtt = rtt.seconds + rtt.microseconds*10**-6
                    print("RTT = ",rtt, "s")
                    socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    socket.bind(('0.0.0.0', 8787))
                    nomFichier = socket.recv(255)
                    contenu,tailleFichier = lectureFichier(nomFichier)
                    listeMessage = fragmentationFichier(contenu,tailleFichier)
                    del contenu
                    miseEnCache = 0
                    print("taille : ",len(listeMessage))

                    cwnd = 1 #congestion window
                    cwndwrite = cwnd
                    rto = rtt*10   
                    # rto = 0.5
                    numDernierAck = 0
                    messageRecu = [1]
                    pertePaquet = 0
                    duplicateACK = 0
                    i=0

                    for i in range(cwnd):
                        message = numeroSequenceByte(i) + listeMessage[i]
                        socket.sendto(message,address)
                        print("Envoi message num :",numeroSequenceByte(i)) 

                    i = cwnd - 1


                    while(numDernierAck!=len(listeMessage)): # Tant que le numero du dernier acquittement n'est pas celui du dernier message.
                        # print("boucle")
                        inputs = [socket]                           
                        read,write,error = select.select(inputs,[],[],rto)
                        for s in read: # Si une socket est dispo en lecture.
                            if s is socket:
                                data = s.recv(255)
                                print(data)
                                data=data.decode()
                                data = data[:data.find('\x00')]
                                if(int(data[3:])==numDernierAck):
                                    duplicateACK = duplicateACK+1
                                    if(duplicateACK==3):
                                        if(i<len(listeMessage)):
                                            print("--------- Duplicate ACK ---------")
                                            message = numeroSequenceByte(i) + listeMessage[i]
                                            socket.sendto(message,address)
                                            pertePaquet = pertePaquet + 1
                                            print("Retransmission ",numeroSequenceByte(i))

                                if(int(data[3:])>numDernierAck):
                                    numDernierAck = int(data[3:])
                                    print("ACK "+str(numDernierAck)+" recue")
                                    if(numDernierAck not in messageRecu):
                                        messageRecu.append(numDernierAck)
                                        for k in range(messageRecu[-2],messageRecu[-1]):
                                            cwnd = cwnd +1
                                            print("cwnd: ",cwnd,"k:",k)
                                            indexEnvoi = k+cwnd-1
                                            if(indexEnvoi<len(listeMessage)):
                                                message = numeroSequenceByte(indexEnvoi) + listeMessage[indexEnvoi]
                                                socket.sendto(message,address)
                                                print("Envoi: ",indexEnvoi+1)

                                            indexEnvoi = k+cwnd

                                            if(indexEnvoi<len(listeMessage)):
                                                message = numeroSequenceByte(indexEnvoi) + listeMessage[indexEnvoi]
                                                socket.sendto(message,address)
                                                print("Envoi: ",indexEnvoi+1)


                                    i = numDernierAck



                        if(len(read)==0):
                            print("--------- Perte de paquet ---------")
                            pertePaquet = pertePaquet + 1
                           # cwnd = int(floor(cwnd/2))
                            cwnd = 1
                            i = numDernierAck
                            if(i<len(listeMessage)):
                                message = numeroSequenceByte(i) + listeMessage[i]
                                socket.sendto(message,address)
                                print("Retransmission ",numeroSequenceByte(i))



                    socket.sendto(b'FIN',address)
                    continu = False




print ("Close")
print("|==========================================|")
print("RTT:",rtt*10**6," us")
t2 = datetime.now()
tempsTotal = (t2 - t1)
#tailleFichier = os.path.getsize(nomFichier)
print("Taille totale fichier (en octets):",tailleFichier)
tempsTotal = tempsTotal.seconds + tempsTotal.microseconds*10**-6
print("Temps transmission:",tempsTotal)
print("Debit (Ko/s):",(tailleFichier/tempsTotal)*10**-3,"Ko/s")
print("Debit (Kb/s):",(tailleFichier/tempsTotal)*10**-3*8,"Kb/s")
print("Nombre de retransmissions:",pertePaquet)
print("|==========================================|")
resultats = open("resultats.csv", "a")
resultats.write(str(rto*10**6) + ";" + str(cwndwrite) + ";" + str(round((tailleFichier/tempsTotal)*10**-3, 3)) + ";" + str(pertePaquet) + ";" + str(rtt*10**6) + "\n")
resultats.close()
serversocket.close()



# fragmentationFichier(contenu,nomFichier)
