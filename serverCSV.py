import socket
import select
from datetime import datetime
import os
import sys

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



port = int(sys.argv[1])
# create an INET, STREAMing socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# bind the socket to a public host, and a well-known port
serversocket.bind(('0.0.0.0', port))
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
                        rtt = rtt.seconds + rtt.microseconds*10**-6
                        print("RTT = ",rtt, "s")
                        socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        socket.bind(('0.0.0.0', 8787))
                        nomFichier = socket.recv(255)
                        contenu,nomFichier = lectureFichier(nomFichier)
                        listeMessage = fragmentationFichier(contenu,nomFichier)
                        print("taille : ",len(listeMessage))

                        cwnd = 1 #congestion window
                        cwndwrite = cwnd
                        swnd = 1 #sliding window
                        rto = rtt*20
                        sstresh = 32
                        # rto = 0.5
                        numDernierAck = 0
                        messageEnvoi = []
                        messageRecu = [1]
                        pertePaquet = 0
                        i=0

                        while(i<len(listeMessage)): # Tant qu'on n'a pas envoye tout les messages.
                            message = numeroSequenceByte(i) + listeMessage[i]
                            socket.sendto(message,address)
                            messageEnvoi.append(i)
                            # print("SWND:",swnd,i)
                            print("Num sequence envoye:",numeroSequenceByte(i))
                            i = i+swnd-1
                            # print("i: ",i)


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
                                            if(numDernierAck not in messageRecu):
                                                messageRecu.append(numDernierAck)

                                                # messageEnvoi.remove(numDernierAck)
                                                # messageEnvoi.append(numDernierAck+cwnd,numDernierAck+cwnd+1)
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
                                            # if(i<len(listeMessage)):
                                            #     message = numeroSequenceByte(i) + listeMessage[i]
                                            #     socket.sendto(message,address)



                                if(len(read)==0):
                                    print("--------- Perte de paquet ---------")
                                    pertePaquet = pertePaquet + 1
                                    cwnd = 1
                                    # socket.sendto(message,address)
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
tailleFichier = os.path.getsize(nomFichier)
print("Taille totale fichier (en octets):",tailleFichier)
tempsTotal = tempsTotal.seconds + tempsTotal.microseconds*10**-6
print("Temps transmission:",tempsTotal)
print("Debit (Ko/s):",(tailleFichier/tempsTotal)*10**-3,"Ko/s")
print("Debit (Kb/s):",(tailleFichier/tempsTotal)*10**-3*8,"Kb/s")
print("Nombre de retransmissions:",pertePaquet)
print("|==========================================|")
g = open("resultats.csv", "a")
g.write(str(rto*10**6) + ";" + str(cwndwrite) + ";" + str(round((tailleFichier/tempsTotal)*10**-3, 3)) + ";" + str(pertePaquet) + ";" + str(rtt*10**6) + "\n")
g.close()
serversocket.close()


# fragmentationFichier(contenu,nomFichier)
