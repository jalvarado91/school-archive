# TCPServer.py
import os
import time
from socket import socket, SOCK_STREAM, AF_INET
from datetime import datetime

serverPort = 1234

cookie_store = "cookie_flavor=oreo;someother_cookie=cool"

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
            #filename = headers[0].split()[1].partition("/")[2]
            filename = "cookieshow.html"
            fpath = os.path.join('.', filename)
            if not os.path.isfile(fpath):
                raise IOError
            if 'Cookie' in headers_dict:
                cookie_content = headers_dict['Cookie']
                cookie_store = cookie_content
            sendFile(connectionSocket, fpath, "text/html; charset=utf-8")
            connectionSocket.close()
        except IOError:
            print "Not found %s" % filename
            sendError(connectionSocket, '404', 'Not Found')
            connectionSocket.close()
        except KeyboardInterrupt:
            print "\nInterrupted by CTRL-C"
            break
    serverSocket.close()

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
    print "Listening on port", port
    print "Interrupt with CTRL-C"
    return serverSocket

def sendFile(connectionSocket, filename, content_type):
    curr_time = datetime.now()

    path = os.path.join('.', filename)
    file_handle = open(path)
    data = file_handle.read()
    file_handle.close()

    last_modified = datetime.fromtimestamp(os.path.getmtime(path))
    
    
    cookies_dict = deserialize_cookies(cookie_store)
    cookies_display = makeCookiesList(cookies_dict)

    data = data.replace("{{cookies_values}}", cookies_display)

    data_len = len(data)

    response =  "HTTP/1.1 200 OK\r\n"\
                "Date: {0}\r\n"\
                "Server: JuanAlvarado/1.0.0 FIU (Ubuntu)\r\n"\
                "Content-Type: {1}\r\n"\
                "Content-Length: {2}\r\n"\
                "Last-Modified: {3}\r\n"\
                "Set-Cookie: {4}\r\n"\
                "\r\n"\
                "{5}".format(
                        curr_time.strftime("%a, %d %b %Y %I:%M:%S"),
                        content_type,
                        data_len,
                        last_modified.strftime("%a, %d %b %Y %I:%M:%S"),
                        cookie_store,
                        data
                    )
    connectionSocket.send(response)

def makeCookiesList(cookie_dict):
    cookies_display = "<ul>\n"
    for key in cookie_dict:
        list_item = "<li>"+key+": "+cookie_dict[key]+"</li>\n"
        cookies_display += list_item
    cookies_display += "</ul>"

    return cookies_display

def deserialize_cookies(cookie_data):
    key_pairs = cookie_data.strip().split(';')
    key_val_pairs = {}
    for pair in key_pairs:
        parts = pair.split('=')
        if len(parts) == 2:
            key_val_pairs[parts[0].strip()] = parts[1].strip()
    return key_val_pairs

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
