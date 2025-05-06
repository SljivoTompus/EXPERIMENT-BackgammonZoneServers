import socket
import struct


class ZoneGameServer:
    def __init__(self, host='192.168.0.102', port=28805):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = []
        self.game = ZoneGame()

    def start_server(self):
        """Start the server and listen for incoming connections."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server started on {self.host}:{self.port}")

        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"New connection from {client_address}")
            self.clients.append(client_socket)
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def send_handshake(self, client_socket):
        """Send the first handshake message."""
        # Magic value and checksum (dummy values for now, need to be replaced with actual)
        magic_value = b"\x01\x02\x03\x04"  # Sample magic value (4 bytes)
        checksum = b"\x00\x00\x00\x00"  # Sample checksum (4 bytes)

        # Paket sa svim nulama
        first_packet = b"\x00" * 0x28  # Create a packet of size 0x28 (40 bytes)

        # Zameni magic i checksum vrednosti u odgovarajuća mesta u paketu
        handshake_packet = first_packet[:8] + magic_value + first_packet[12:24] + checksum + first_packet[28:]

        # Pošaljemo paket klijentu
        client_socket.sendall(handshake_packet)
        print("Handshake sent to client.")

    def handle_client(self, client_socket):
        """Handle communication with a single client."""
        try:
            # Send the first handshake message
            self.send_handshake(client_socket)

            # Čekaj na odgovor
            data = client_socket.recv(1024)
            if data:
                decoded_data = data.decode('windows-1252', errors='ignore')
                print(f"Received data: {decoded_data}")
                # Nastavi sa obradom podataka...
            else:
                print("No data received, closing connection.")
        except Exception as e:
            print(f"Error while handling client: {e}")
        finally:
            try:
                client_socket.close()
                print("Client socket closed.")
            except Exception as e:
                print(f"Error closing socket: {e}")

    def stop_server(self):
        """Stop the server and close all connections."""
        print("Stopping the server...")
        for client_socket in self.clients:
            try:
                client_socket.close()
                print(f"Closed connection with {client_socket}")
            except Exception as e:
                print(f"Error closing client socket: {e}")
        try:
            self.server_socket.close()
            print("Server socket closed.")
        except Exception as e:
            print(f"Error closing server socket: {e}")


# Pokretanje servera
if __name__ == "__main__":
    server = ZoneGameServer()
    server.start_server()
