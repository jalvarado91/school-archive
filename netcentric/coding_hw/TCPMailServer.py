# TCPMailServer.py
import os
import time
import re
import binascii
from socket import socket, SOCK_STREAM, AF_INET
from datetime import datetime

from MailServer import send_email

serverPort = 1234

def main():
    serverSocket = openTcpSocket(serverPort)
    while True:
        try:
            connectionSocket, addr = serverSocket.accept()
            message = connectionSocket.recv(4096)
            msg = message.split('\r\n\r\n')
            hds = msg[0]
            body = ''
            if len(msg) > 1:
                body = msg[1]
            headers = hds.split('\r\n')
            headers_dict = makeDict(headers)
            request = headers[0].split()
            req_path = request[1].partition("?")
            filename = req_path[0].partition("/")[2]
            query = req_path[2]
            if query:
                qs_params = make_querystring_dict(query)
                #send_email("Juan Alvarado", "jalvarado91@gmail.com", "Yoo dawg", "This is another test fam")
                send_email(qs_params['from'], qs_params['email'], qs_params['subject'], qs_params['message'])
                sendFile(connectionSocket, filename, "text/html; charset=utf-8")
                connectionSocket.close()
        except IOError:
            print "Not found %s" % filename
            sendError(connectionSocket, '404', 'Not Found')
            connectionSocket.close()
        except KeyboardInterrupt:
            print "\nInterrupted by CTRL-C"
            break
    serverSocket.close()

def decode_query(query):
    value = re.sub(r'[+]', ' ', query)
    value = re.sub(r'%[0-9a-fA-F]{2}', transpile_ascii, value)
    return value

def transpile_ascii(value):
    value = value.group()
    return binascii.unhexlify(value[1:3])

def make_querystring_dict(qs):
    qs = qs.split('&')
    qs_params = {}
    for pair in qs:
        keyval = pair.split('=')
        qs_params[keyval[0]] = decode_query(keyval[1])
    return qs_params

def makeDict(headers):
    headers = headers[1:]
    header_map = {}
    for header in headers:
        if len(header) >= 2:
            pair = header.split(':', 1)
            header_name = pair[0]
            header_cont = pair[1].lstrip()
            header_map[header_name] = header_cont
    return header_map

def openTcpSocket(port):
    # Create a UDP socket
    serverSocket = socket(AF_INET, SOCK_STREAM)
    # Assign IP address and port to socket
    serverSocket.bind(('', port))
    serverSocket.listen(1)
    print "Interrupt with CTRL-C"
    return serverSocket

def sendFile(connectionSocket, filename, content_type):
    curr_time = datetime.now()

    path = os.path.join('.', filename)
    file_handle = open(path)
    data = file_handle.read()
    file_handle.close()

    last_modified = datetime.fromtimestamp(os.path.getmtime(path))

    data_len = len(data)

    response =  "HTTP/1.1 200 OK\r\n"\
                "Date: {0}\r\n"\
                "Server: JuanAlvarado/1.0.0 FIU (Ubuntu)\r\n"\
                "Content-Type: {1}\r\n"\
                "Content-Length: {2}\r\n"\
                "Last-Modified: {3}\r\n"\
                "\r\n"\
                "{4}".format(
                        curr_time.strftime("%a, %d %b %Y %I:%M:%S"),
                        content_type,
                        data_len,
                        last_modified.strftime("%a, %d %b %Y %I:%M:%S"),
                        data
                    )
    connectionSocket.send(response)

def sendError(connectionSocket, statusCode, message):
    time = datetime.now()

    response =  "HTTP/1.1 {0} {1}\r\n"\
                "Date: {2}\r\n"\
                "Content-Type: text/plain\r\n"\
                "Server: JuanAlvarado/1.0.0 FIU (Ubuntu)\r\n"\
                "\r\n"\
                "{3}".format(
                        statusCode,
                        message,
                        time.strftime("%a, %d %b %Y %I:%M:%S"),
                        message
                    )
    connectionSocket.send(response)


main()