#!/usr/bin/env python

import json
import socket
from utils import *

# create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

# set a port number
port = 9999

# bind the socket object to the address and port
server_socket.bind((host, port))

# set the maximum number of clients that can be queued up
server_socket.listen(1)

# generate a public/private key pair
key_size = input('Enter key size: ')
e, d, n = generate_key(key_size)

print('Waiting for client connection...')

try:
    # accept a client connection
    client_socket, address = server_socket.accept()
    print(f'Connection established with {address}')

    data = client_socket.recv(1024).decode()
    data = json.loads(data)
    _e, _n = data
    print(_e, _n)
    response = json.dumps([e, n])
    client_socket.send(response.encode())
    
    while True:
        data = client_socket.recv(1024).decode()
        data = json.loads(data)
        plaintext = decrypt(data, d, n)
        print('client: ' + plaintext)

        # send a response back to the client
        response = f'Message Received'
        client_socket.send(response.encode())

        # send data to the client
        data = input('Enter Message: ')
        data = encrypt(data, _e, _n)
        client_socket.send(json.dumps(data).encode())

except KeyboardInterrupt:
    # close the socket on a KeyboardInterupt exception
    server_socket.close()
    print('\nServer socket closed.')