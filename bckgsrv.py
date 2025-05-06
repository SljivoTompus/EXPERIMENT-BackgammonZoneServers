import socket
import threading
import time

# XOR dekripcija sa ključem 0xf8273645
def xor_decrypt(data, key=0xf8273645):
    """XOR dekripcija podataka iz igre."""
    key_bytes = key.to_bytes(4, 'little')  # Konvertujemo ključ u bajtove
    decrypted = bytearray()

    for i in range(len(data)):
        decrypted.append(data[i] ^ key_bytes[i % 4])  # XOR svaki bajt sa ključem
    return bytes(decrypted)

class ZoneGameServer:
    def __init__(self, host='192.168.1.73', port=28805):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = []
        self.lobby = []  # Lista igrača koji čekaju protivnika
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
            threading.Thread(target=self.handle_client, args=(client_socket, client_address)).start()

    def handle_client(self, client_socket, client_address):
        """Handle communication with a single client."""
        try:
            # Handshake sa klijentom
            if not self.perform_handshake(client_socket):
                print("Handshake failed. Closing connection.")
                client_socket.close()
                return

            # Dodaj klijenta u lobby nakon uspešnog handshake-a
            player_id = len(self.lobby) + 1
            self.lobby.append({"id": player_id, "socket": client_socket, "ip": client_address})
            print(f"Player {player_id} added to lobby. Total players: {len(self.lobby)}")

            # Pokušaj da pronađeš protivnika
            self.match_players()

            while True:
                data = client_socket.recv(1024)
                if not data:
                    break  # Klijent zatvorio konekciju

                # Dekodiranje dolaznih podataka
                decrypted_data = xor_decrypt(data)
                print(f"Received decrypted data: {decrypted_data}")

                # Obradi poruku kroz ZoneClientGameProcessMessage
                self.ZoneClientGameProcessMessage(decrypted_data, client_socket)

        except Exception as e:
            print(f"Error while handling client: {e}")
        finally:
            try:
                client_socket.close()
                print("Client socket closed.")
                self.lobby = [p for p in self.lobby if p["socket"] != client_socket]  # Izbaci klijenta iz lobija
            except Exception as e:
                print(f"Error closing socket: {e}")

    def perform_handshake(self, client_socket):
        """Perform handshake with the client."""
        try:
            handshake_request = client_socket.recv(1024)
            if not handshake_request:
                print("No handshake request received.")
                return False

            print(f"Raw handshake request: {handshake_request}")
            decrypted_request = xor_decrypt(handshake_request)

            print(f"Decrypted handshake request: {decrypted_request}")

            # Proveri da li handshake sadrži "ZoNe"
            if decrypted_request[:4] == b"ZoNe":
                print("Handshake recognized as valid ZoNe protocol.")

            # Pošalji odgovor klijentu
            handshake_response = xor_decrypt(b"ZoNeHandshakeSuccess")
            client_socket.sendall(handshake_response)
            print("Handshake completed successfully. Sent response to client.")

            return True

        except Exception as e:
            print(f"Error during handshake: {e}")
            return False

    def ZoneClientGameProcessMessage(self, data, client_socket):
        """Obrada dolaznih poruka od klijenta."""
        if data.startswith(b"FirstMsg"):
            print("Client sent FirstMsg, responding...")
            client_socket.sendall(xor_decrypt(b"FirstMsg_Ack"))

        elif data.startswith(b"FindMatch"):
            print("Client is looking for a match...")
            self.match_players()

        elif data.startswith(b"StartGame"):
            print("Starting game session...")
            self.game.ZoneClientMain()

        else:
            print(f"Unknown message received: {data}")

    def match_players(self):
        """Proverava da li ima dovoljno igrača za meč."""
        if len(self.lobby) >= 2:
            p1, p2 = self.lobby[:2]
            print(f"Match found: Player {p1['id']} vs Player {p2['id']}")

            # Pošalji poruku obema stranama da započnu igru
            p1["socket"].sendall(xor_decrypt(b"GameStart"))
            p2["socket"].sendall(xor_decrypt(b"GameStart"))

            # Izbaci ih iz lobija jer su našli meč
            self.lobby = self.lobby[2:]

class ZoneGame:
    def __init__(self):
        self.game_global_pointer = None
        self.client_global_pointer = None

    def ZGetGameGlobalPointer(self):
        """Retrieve the game global pointer."""
        if self.game_global_pointer is None:
            print("Warning: Game global pointer is not set!")
            self.ZSetGameGlobalPointer('DefaultPointer')
        return self.game_global_pointer

    def ZGetClientGlobalPointer(self):
        """Retrieve the client global pointer."""
        return self.client_global_pointer

    def ZSetGameGlobalPointer(self, pointer):
        """Set the game global pointer."""
        self.game_global_pointer = pointer
        print(f"Game global pointer set to: {self.game_global_pointer}")

    def ZoneClientMessageHandler(self):
        """Simulate handling a message for the client."""
        print("Handling message for the client...")

    def ZoneClientMain(self):
        """Pokreće glavnu petlju igre kada se pronađe protivnik."""
        game_pointer = self.ZGetGameGlobalPointer()
        if game_pointer:
            print(f"ZoneClientMain: Game started with pointer: {game_pointer}")
            self.ZoneClientMessageHandler()
        else:
            print("Failed to retrieve game global pointer.")

if __name__ == "__main__":
    server = ZoneGameServer()

    try:
        threading.Thread(target=server.start_server, daemon=True).start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.start_server()
