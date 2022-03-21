#!/usr/bin/env python3

import socket
import sys
import select
import os.path
from os import path
from os.path import exists

from file_reader import FileReader


class Jewel:

    # Note, this starter example of using the socket is very simple and
    # insufficient for implementing the project. You will have to modify this
    # code.
    def __init__(self, port, file_path, file_reader):
        self.file_path = file_path
        self.file_reader = file_reader

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ip = socket.gethostname()
        server.bind((ip, port))


        server.listen(5)
        print('Listening on port %s ...' % port)

        inputs = [server]
        outputs = list()

        while True:
            read_ready, write_ready, exceptions = select.select(inputs, outputs, [])
            for s in read_ready:
                if s is server:
                    # Wait for client connections
                    client_connection, client_address = s.accept()

                    print('[CONN] Connection from ' + client_address[0] + ' on port ' + str(client_address[1]))
                    # Get the client request
                    request = client_connection.recv(1024).decode()

                    # parse incoming HTTP request
                    header_end = request.find('\r\n\r\n')
                    if header_end > -1:
                        header_string = request[:header_end]
                        lines = header_string.split('\r\n')

                        request_fields = lines[0].split()
                        headers = lines[1:]

                        #print(request_fields)

                    # Send HTTP response
                    response = ''
                    data = ''
                    requested_object = request_fields[1][1:]
                    print('[REQU] [' + client_address[0] + ':' + str(client_address[1]) + '] ' + request_fields[0] + ' request for ' + file_path + requested_object)

                    # if it is a file, send header for file
                    if path.isfile(requested_object):
                        if exists(requested_object):
                            filetype = requested_object.split('.')[1]
                            mime = ''
                            if filetype == 'html':
                                mime = 'text/html'
                            if filetype == 'css':
                                mime = 'text/css'
                            if filetype == 'png':
                                mime = 'image/png'
                            if filetype == 'jpg':
                                mime = 'image/jpg'
                            if filetype == 'gif':
                                mime = 'image/gif'
                            length = str(os.path.getsize(requested_object))
                            response = 'HTTP/1.0 200 OK\nCotent-Length: ' + length + '\nContent-Type: ' + mime + '\n\n'

                            data = file_reader.get(requested_object, 0)

                    # if it is a directory, send simple html with directory
                    elif os.path.isdir(requested_object):
                        response = 'HTTP/1.0 200 OK\n\n<html><body><h1>' + file_path + requested_object + '</h1></body></html>'

                    # if file/path not found, send 404
                    else:
                        print('[ERRO] [' + client_address[0] + ':' + str(client_address[1]) + '] ' + request_fields[0] + ' returned error 404')
                        response = 'HTTP/1.0 404\n\n<html><body><h1>404 Not Found</h1></body></html>'

                    # if request not implemented, send 501
                    # if invalid request, send 400
                    implemented_requests = ['GET', 'HEAD']
                    unimplemented_requests = ['POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATFCH']
                    # if invalid request return 400 invalid request
                    if request_fields[0] not in implemented_requests:
                        if request_fields[0] in unimplemented_requests:
                            print('[ERRO] [' + client_address[0] + ':' + str(client_address[1]) + '] ' + request_fields[
                                0] + ' returned error 501')
                            response = 'HTTP/1.0 501 Method Unimplemented\n\n<html><body><h1>501 Method Unimplemented</h1></body></html>'
                        else:
                            print('[ERRO] [' + client_address[0] + ':' + str(client_address[1]) + '] ' + request_fields[
                                0] + ' returned error 400')
                            response = 'HTTP/1.0 400 Invalid Request\n\n<html><body><h1>400 Invalid Request</h1></body></html>'

                    client_connection.sendall(response.encode())

                    # if have data and requested file, send it
                    if data is not None and path.isfile(requested_object):
                        client_connection.send(data)

        # Close socket
        server.close()

if __name__ == "__main__":
    FR = FileReader()

    J = Jewel(8000, './', FR)
