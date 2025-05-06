import socket

HOST = '192.168.0.102'
PORT = 28805

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()
        print(f"Server started on {HOST}:{PORT}")
        
        while True:
            conn, addr = server.accept()
            print(f"Connection attempt from {addr}")
            data = conn.recv(1024)
            if data == b"STOP":
                print("Stopping server...")
                break  # Izlazi iz petlje i zatvara server
            conn.sendall(b"Hello from server!")
except KeyboardInterrupt:
    print("Server manually stopped with Ctrl+C")
