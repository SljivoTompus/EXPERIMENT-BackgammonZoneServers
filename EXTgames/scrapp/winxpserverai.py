import socket

HOST = '192.168.0.102'  # Sluša na svim interfejsima
PORT = 28805      # Ovaj port treba da bude isti kao port igre

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Omogućava ponovno korišćenje porta
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server started on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()  # Prihvata vezu od klijenta
        print(f"Connection attempt from {addr}")  # Ovde beleži ko pokušava da se poveže
        data = conn.recv(1024)  # Prima podatke od klijenta
        if data:
            print(f"Received data: {data}")  # Ispisuje primljene podatke
            conn.sendall(b"Hello from server!")  # Odgovara klijentu
