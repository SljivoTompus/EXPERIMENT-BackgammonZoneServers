import socket

HOST = '192.168.0.102'  # Tvoja lokalna IP adresa
PORT = 28805  # Port na kojem server sluša

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()
        print(f"Server pokrenut na {HOST}:{PORT}")

        while True:
            conn, addr = server.accept()
            with conn:
                print(f"Veza sa {addr}")
                data = conn.recv(1024)
                if data:
                    print(f"Primljeno: {data}")
                    conn.sendall(b"Mock odgovor od servera")
except socket.error as e:
    print(f"Greška pri povezivanju sa serverom: {e}")
