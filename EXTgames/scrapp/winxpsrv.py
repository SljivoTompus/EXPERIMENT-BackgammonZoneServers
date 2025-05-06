import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('192.168.0.102', 28805))
server.listen(1)

print("Server is listening on port 28805...")
while True:
    client_socket, client_address = server.accept()
    print(f"Connection from {client_address}")
    data = client_socket.recv(1024)
    print(f"Received: {data}")
    client_socket.close()
