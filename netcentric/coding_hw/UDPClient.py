from socket import socket, SOCK_DGRAM, AF_INET, timeout
import time

serverName = 'ocelot.aul.fiu.edu'
serverPort = 1235

def sendMessage(message, clientSocket):
    start_time = time.time()
    clientSocket.sendto(message, (serverName, serverPort))
    try:
        modifiedMessage, addr = clientSocket.recvfrom(2048)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print "received: ", modifiedMessage
        print "ellapsed: ", elapsed_time
    except timeout:
        end_time = time.time()
        elapsed_time = end_time - start_time
        print "timedout: ", elapsed_time

def main():
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.settimeout(1)
    message = raw_input('Input lowercase sentence: ')
    for i in range(10):
        sendMessage(message, clientSocket)
    clientSocket.close()

main()