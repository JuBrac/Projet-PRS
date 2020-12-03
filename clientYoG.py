# coding: utf-8

import socket
import time

hote = "localhost"
port = 2020

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket.connect((hote, port))
print ("Connection on {}".format(port))

socket.send(b'SYN')
synAck = socket.recv(255)
socket.send(b'ACK')
print(synAck)
synAck = str(synAck)
port = int(synAck[9:13])
print(port)
socket.connect((hote, port))
socket.send(b'test.txt')

print ("Close")
socket.close()