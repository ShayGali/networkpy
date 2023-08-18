import socket

SERVER_IP = "0.0.0.0"  # listen on all interfaces
PORT = 8821
MAX_MSG_SIZE = 1024

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# same as bind in TCP - associate the socket with the ip and the port
server_socket.bind((SERVER_IP, PORT))

# receive the message from the client
(client_message, client_address) = server_socket.recvfrom(MAX_MSG_SIZE)
# decode the message from bytes to string
data = client_message.decode()
print("Client sent: " + data)
response = "Hello " + data

# send the response to the client
server_socket.sendto(response.encode(), client_address)

# close the socket
server_socket.close()
