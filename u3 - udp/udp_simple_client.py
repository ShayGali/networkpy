import socket

SERVER_IP = "127.0.0.1"
PORT = 8821
MAX_MSG_SIZE = 1024

# SOCK_DGRAM is the socket type to use for UDP sockets
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# here we don't need to connect, just send the message with sendto() method
my_socket.sendto("Shay".encode(), (SERVER_IP, PORT))

# receive the message from the server
"""
recvfrom() returns a tuple of two elements.
The first is the message itself,
and the second is the address of the socket from which it was sent.
"""
(response, remote_address) = my_socket.recvfrom(MAX_MSG_SIZE)
data = response.decode()  # decode the message from bytes to string
print("The server sent " + data)

# close the socket
my_socket.close()
