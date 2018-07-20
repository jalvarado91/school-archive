#!/usr/bin/python

import sys
import os
from MailServer import send_email

sys.stderr = sys.stdout


def readHeaders():
    environ = os.environ
    request_method = environ["REQUEST_METHOD"]
    if environ["QUERY_STRING"] == "":
        query_string = None
    else:
        query_string = environ["QUERY_STRING"]

    return {
        method: request_method,
        query_string: query_string
    }


def sendFile(connectionSocket, filename, content_type):
    curr_time = datetime.now()

    path = os.path.join('.', filename)
    file_handle = open(path)
    data = file_handle.read()
    file_handle.close()

    last_modified = datetime.fromtimestamp(os.path.getmtime(path))

    data_len = len(data)

    response = "HTTP/1.1 200 OK\r\n"\
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

    response = "HTTP/1.1 {0} {1}\r\n"\
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


def main():
    serverSocket = openTcpSocket(serverPort)
    while True:
        try:
            connectionSocket, addr = serverSocket.accept()
            filename = "index.html"
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


main()
