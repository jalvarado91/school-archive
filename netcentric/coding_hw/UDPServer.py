from socket import socket, SOCK_DGRAM, AF_INET
import random

serverSocket = socket(AF_INET, SOCK_DGRAM)

serverSocket.bind(('', 1235))

print "Waiting for connections"
while True:
    message, address = serverSocket.recvfrom(2048)
    chance = random.randint(0,10)
    if chance >= 4:
        print message, address
        message = message.upper()
        serverSocket.sendto(message, address)

serverSocket.close()
