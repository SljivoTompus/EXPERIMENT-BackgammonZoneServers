import socket
import threading
import base64


class ZoneGameServer:
    def __init__(self, host='192.168.0.103', port=28805):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = []

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

    def handle_client(self, client_socket):
        """Handle communication with a single client."""
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break  # Client closed connection

                print(f"Received data (raw bytes): {data}")

                # Pokusaj sa različitim dekodiranjima
                try:
                    decoded_data_utf8 = data.decode('utf-8')
                    print(f"Decoded as UTF-8: {decoded_data_utf8}")
                except Exception as e:
                    print(f"Error decoding as UTF-8: {e}")

                try:
                    decoded_data_ascii = data.decode('ascii')
                    print(f"Decoded as ASCII: {decoded_data_ascii}")
                except Exception as e:
                    print(f"Error decoding as ASCII: {e}")

                try:
                    decoded_data_latin1 = data.decode('latin-1')
                    print(f"Decoded as Latin-1: {decoded_data_latin1}")
                except Exception as e:
                    print(f"Error decoding as Latin-1: {e}")

                # Base64 decoding
                try:
                    decoded_data_base64 = base64.b64encode(data)
                    print(f"Decoded as base64: {decoded_data_base64}")
                except Exception as e:
                    print(f"Error decoding as base64: {e}")

                # Process message further
                print("Handling message for the client...")

                # Simuliraj obradu poruka
                print(f"Message processed")

                # Odgovori klijentu
                client_socket.sendall(b"Message processed")

        except Exception as e:
            print(f"Error while handling client: {e}")
        finally:
            client_socket.close()

    def stop_server(self):
        """Stop the server and close all connections."""
        print("Stopping the server...")
        for client_socket in self.clients:
            client_socket.close()
        self.server_socket.close()


if __name__ == "__main__":
    # Pokreni server
    server = ZoneGameServer()

    try:
        # Start the server in a separate thread to allow client connections
        threading.Thread(target=server.start_server, daemon=True).start()

        # Allow server to run indefinitely
        while True:
            pass

    except KeyboardInterrupt:
        # Stop server gracefully on keyboard interrupt (Ctrl+C)
        server.stop_server()
