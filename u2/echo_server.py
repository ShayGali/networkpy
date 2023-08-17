import socket

ip = "127.0.0.1"  # localhost
port = 8820

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind((ip, port))

# Listen for incoming connections
server_socket.listen()

print(f"Listening on {ip}:{port}")

# Wait for a connection
(client_socket, client_address) = server_socket.accept()
"""
client_socket - object that represent socket for communication with client
client_address - tuple of client ip and port
"""

print(f"Connected to {client_address}")

# Receive data from the client
data = client_socket.recv(1024).decode()  # decode() - convert bytes to string

print(f"Client send: {data}")

# Send the received data back to the client
client_socket.send(data.encode())  # encode() - convert string to bytes

# Close the connection with the client
client_socket.close()
print(f"Disconnected from {client_address}")

# Close the server socket
server_socket.close()
print("Server socket closed")

""" for keep listing for new clients

# Wait for a connection
while True:
    # Accept a new connection
    client_socket, client_address = server_socket.accept()
    print(f"Connected to {client_address}")
    while True:
        # Receive data from the client
        data = client_socket.recv(1024)
        if not data:
            break
        # Send the received data back to the client
        client_socket.sendall(data)
    print(f"Disconnected from {client_address}")
    client_socket.close()


"""
