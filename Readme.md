# RSA Public-Key Cryptosystem

_This is a simple application for exchanging messages securely over a network using RSA encryption._

## Usage

To start the application, open two terminal windows and run the following commands:

In the 1st terminal: `python server.py`
In the 2nd terminal: `python client.py`

You will be prompted to enter the size of the RSA key to be used for encryption. Enter a the size of the key you want to use for each user.

Once the application starts, it will listen for incoming connections on the receive port and prompt you to enter a message to send over the send port. The message will be encoded then encrypted using the RSA key and sent over the network to the other end of the connection, where it will be decrypted then decoded and printed to the console.