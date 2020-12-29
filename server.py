import socket
import select
from datetime import datetime
import os

def fragmentationFichier(contenu,nomFichier):


    tailleFichier = os.path.getsize(nomFichier)
    nbSegments = int(tailleFichier/1494)+1
    arrayFrame = []
    # contenu = '\n'.join(contenu)
    contenu = contenu.encode("utf-8")


    for i in range(nbSegments):
        arrayFrame.append(contenu[i*1494:i*1494+1494])

        # arrayFrame[i]= arrayFrame[i].encode("utf-8")
        # print(len(arrayFrame[i]))
    return arrayFrame

def lectureFichier(nomFichier):
    nomFichier = nomFichier.decode("utf-8")
    # print(nomFichier[:nomFichier.find("\x00")])
    nomFichier = nomFichier[:nomFichier.find("\x00")]
    f = open(nomFichier, "r")
    contenu = f.read()
    return contenu,nomFichier


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
                        # t2 = time.perf_counter()
                        t2 = datetime.now()
                        print("ACK recu")
                        rtt = (t2-t1)
                        rtt = rtt.microseconds
                        # print(type(rtt))
                        print("RTT = ",rtt, "us")
                        socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        socket.bind(('0.0.0.0', 8787))
                        nomFichier = socket.recv(255)
                        # socket.setblocking(False)
                        contenu,nomFichier = lectureFichier(nomFichier)
                        listeMessage = fragmentationFichier(contenu,nomFichier)
                        swnd = 16
                        numDernierAck = 0
                        i=0
                        while(i<len(listeMessage)):
                            for j in range(swnd):
                                numSequence = str(j+1)
                                while len(numSequence) < 6 :
                                        numSequence = "0"+numSequence
                                numSequenceByte = numSequence.encode("utf-8")
                                # if(i<len(listeMessage)):
                                message = numSequenceByte + listeMessage[j]
                                socket.sendto(message,address)
                                print("SWND:",swnd,i)
                                print("Num sequence envoye:",numSequence)
                            i = i+swnd-1
                            print("i: ",i)

                            ackRecu=0
                            pertePaquet = 0
                            while(numDernierAck!=len(listeMessage)):
                                # print("boucle")
                                inputs = [socket]
                                read,write,error = select.select(inputs,[],[],rtt*5*10**-6)
                                for s in read:
                                    if s is socket:
                                        data = s.recv(255)
                                        print(data)
                                        if len(data)!=0:
                                            data=data.decode()
                                            data = data[:data.find('\x00')]
                                            if(int(data[3:])>numDernierAck):
                                                numDernierAck = int(data[3:])
                                                print("ACK "+str(numDernierAck)+" recue")
                                                ackRecu=ackRecu+1
                                                i = numDernierAck
                                                numSequence = str(i+1)
                                                while len(numSequence) < 6 :
                                                        numSequence = "0"+numSequence
                                                numSequenceByte = numSequence.encode("utf-8")
                                                if(i<len(listeMessage)):
                                                    message = numSequenceByte + listeMessage[i]
                                                    socket.sendto(message,address)



                                if(len(read)==0):
                                    print("====== Perte de paquet ======")
                                    # socket.sendto(message,address)
                                    try:
                                        numDernierAck = numDernierAck
                                    except NameError:
                                        numDernierAck = 0                                    # swnd = 1
                                    pertePaquet = 1
                                    i = numDernierAck
                                    numSequence = str(i+1)
                                    while len(numSequence) < 6 :
                                            numSequence = "0"+numSequence
                                    numSequenceByte = numSequence.encode("utf-8")
                                    if(i<len(listeMessage)):
                                        message = numSequenceByte + listeMessage[i]
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
