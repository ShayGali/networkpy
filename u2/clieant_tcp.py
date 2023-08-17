import socket

# socket.AF_INET - connect IPv4 address
# socket.SOCK_STREAM - use TCP protocol
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to server
ip = "127.0.0.1"  # localhost
port = 8820
ip_port_tuple = (ip, port)
my_socket.connect(ip_port_tuple)
my_socket.send("Hello server".encode())  # encode() - convert string to bytes

# receive data from server
max_data_size_in_bytes = 1024  # 1 KB - max size of data to receive
data = my_socket.recv(max_data_size_in_bytes).decode()  # decode() - convert bytes to string

print(f'Server send: {data}')

# close socket
my_socket.close()

