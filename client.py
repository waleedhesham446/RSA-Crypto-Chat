#!/usr/bin/env python

import json
import socket
from utils import *

# create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

# set a port number
port = 9999

# generate a public/private key pair
key_size = input('Enter key size: ')
e, d, n = generate_key(key_size)

try:
    # connect to the server
    client_socket.connect((host, port))

    publicKey = [e, n]
    client_socket.send(json.dumps(publicKey).encode())

    # receive a response from the server
    response = client_socket.recv(1024).decode()
    response = json.loads(response)
    _e, _n = response
    print(_e, _n)

    while True:
        # send data to the server
        data = input('Enter Message: ')
        data = encrypt(data, _e, _n)
        client_socket.send(json.dumps(data).encode())

        # receive a response from the server
        response = client_socket.recv(1024).decode()

        # receive data from the server
        message = client_socket.recv(1024).decode()
        message = json.loads(message)
        message = decrypt(message, d, n)
        print(f'server: {message}')

except KeyboardInterrupt:
    # close the socket on a KeyboardInterupt exception
    client_socket.close()
    print('\nServer socket closed.')