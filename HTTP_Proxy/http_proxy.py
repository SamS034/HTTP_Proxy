#!/usr/bin/env python

# CSCI 379 Final Project
# Name: Samuel Shen

from socket import *
from select import *
import sys
import os
import time

serverSocket = socket(AF_INET, SOCK_STREAM)
host = gethostbyname("localhost")
host_port = int(str(sys.argv[1]))
serverSocket.bind((host, host_port))
print('Proxy Server is now started at ip: ', host, 'on port', host_port )

while True:
    serverSocket.listen(1)
    connectionSocket, addr = serverSocket.accept()
    print('Got Connection from', addr)

    data = connectionSocket.recv(1024)
    request_data = data.decode()

    # user request = '/' or '/filename' or /p/fowarding_server(www.google.com)
    request_method = request_data.split(' ')[0] # split the request from a space
    #print('Method: ', request_method)
    #print('Request body: ', request_data)

    if (request_method == 'GET') | (request_method == 'HEAD'):
        file_requested = request_data.split(' ')
        file_requested = file_requested[1]
        print('File Requested: ', file_requested)

        if (file_requested == '/') or (file_requested == '/index.html'):
            try:
                if (request_method == 'GET'):
                    connectionSocket.send(b'HTTP/1.1 200 OK\n')
                    connectionSocket.send(b'Content-Type: text/html\n\n')
                    connectionSocket.send(b'Status code 501: "Not Implemented"')

            except Exception as e:
                if (request_method == 'GET'):
                    connectionSocket.send(b'HTTP/1.1 404 Not Found\n')
                    connectionSocket.send(b'Content-Type: text/html\n')
                    connectionSocket.send(b'Error 404: File not found')

            print("Closing connection with client")
            connectionSocket.close()

        if ("http://www" in file_requested):
            if (request_method == 'GET'):
                message = '\nYour request will be fowarded...\n'

                connectionSocket.send(b'HTTP/1.1 200 OK\n')
                connectionSocket.send(b'Content-Type: text/html\n\n')
                connectionSocket.send(file_requested.encode())
                connectionSocket.send(message.encode())
                connectionSocket.send(request_data.encode())
                time.sleep(5)

                forward_data = request_data.split(" ")[0]
                request_ip = forward_data[1]
                request_ip = str(request_ip)

                port = 80

                forward_ip = gethostbyname_ex(request_ip)

                forwardSocket = socket(AF_INET, SOCK_STREAM)
                forwardSocket.connect((forward_ip, port))
                print("Sucessfully connected to ", forward_ip)
                forwardSocket.send(file_requested.encode())

                data_recv = forwardSocket.recv(1024)
                print("Data Received: ", data_recv)
                data_recv = data_recv.decode()

                connectionSocket.send(data_recv.encode())

                forwardSocket.close()
                connectionSocket.close()

    else:
        print('Unknown HTTP request:', request_method)
serverSocket.close()
