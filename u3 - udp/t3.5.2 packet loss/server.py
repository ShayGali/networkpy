import socket

from util import build_msg, parse_msg, special_sendto, MAX_SERIAL_NUM, TIMEOUT_IN_SECONDS

SERVER_IP = "0.0.0.0"
PORT = 8821
MAX_MSG_SIZE = 1024


server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_IP, PORT))
print("Server is up and listening")


serial_num = 0
while True:
    (client_message, client_address) = server_socket.recvfrom(MAX_MSG_SIZE)
    serial, data = parse_msg(client_message.decode())

    print("Client sent: " + data)
special_sendto(server_socket, data, client_address)

server_socket.close()
print("Server closed")