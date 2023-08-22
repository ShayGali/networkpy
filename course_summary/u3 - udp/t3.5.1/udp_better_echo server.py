import socket

SERVER_IP = "0.0.0.0"
PORT = 8821
MAX_MSG_SIZE = 1024

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_IP, PORT))
print("Server is up and listening")

while True:
    (client_message, client_address) = server_socket.recvfrom(MAX_MSG_SIZE)
    data = client_message.decode()
    print("Client sent: " + data)
    if data == "EXIT":
        server_socket.sendto("BYE".encode(), client_address)
        break

    server_socket.sendto(data.encode(), client_address)

server_socket.close()
print("Server closed")
