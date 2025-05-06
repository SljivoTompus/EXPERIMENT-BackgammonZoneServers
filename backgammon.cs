using System;
using System.Collections.Generic;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

class ZoneGameServer
{
    private string host = "192.168.0.103";
    private int port = 28805;
    private TcpListener server;
    private List<TcpClient> clients = new List<TcpClient>();
    private ZoneGame game = new ZoneGame();

    public void StartServer()
    {
        server = new TcpListener(IPAddress.Parse(host), port);
        server.Start();
        Console.WriteLine($"Server started on {host}:{port}");

        while (true)
        {
            TcpClient client = server.AcceptTcpClient();
            Console.WriteLine("New connection from " + client.Client.RemoteEndPoint);
            clients.Add(client);
            Thread thread = new Thread(() => HandleClient(client));
            thread.Start();
        }
    }

    private void HandleClient(TcpClient client)
    {
        try
        {
            NetworkStream stream = client.GetStream();

            // Handshake
            if (!PerformHandshake(stream))
            {
                Console.WriteLine("Handshake failed. Closing connection.");
                client.Close();
                return;
            }

            // Game communication loop
            byte[] buffer = new byte[1024];
            while (true)
            {
                int bytesRead = stream.Read(buffer, 0, buffer.Length);
                if (bytesRead == 0) break;

                string receivedData = Encoding.GetEncoding("windows-1252").GetString(buffer, 0, bytesRead);
                Console.WriteLine("Received data: " + receivedData);

                game.ZoneClientMessageHandler();
                game.ZoneClientMain();

                byte[] response = Encoding.ASCII.GetBytes("Message processed");
                stream.Write(response, 0, response.Length);
            }
        }
        catch (Exception e)
        {
            Console.WriteLine("Error while handling client: " + e.Message);
        }
        finally
        {
            client.Close();
            Console.WriteLine("Client socket closed.");
        }
    }

    private bool PerformHandshake(NetworkStream stream)
    {
        try
        {
            byte[] buffer = new byte[1024];
            int bytesRead = stream.Read(buffer, 0, buffer.Length);
            if (bytesRead == 0) return false;

            byte[] handshakeRequest = new byte[bytesRead];
            Array.Copy(buffer, handshakeRequest, bytesRead);

            Console.WriteLine("Received handshake request: " + BitConverter.ToString(handshakeRequest));

            byte[] expectedVersion = Encoding.ASCII.GetBytes("HandshakeKey");
            if (!CompareByteArrays(handshakeRequest, expectedVersion))
            {
                Console.WriteLine("Invalid handshake.");
                return false;
            }

            byte[] handshakeResponse = Encoding.ASCII.GetBytes("Handshake successful");
            stream.Write(handshakeResponse, 0, handshakeResponse.Length);
            Console.WriteLine("Handshake completed successfully.");
            return true;
        }
        catch (Exception e)
        {
            Console.WriteLine("Error during handshake: " + e.Message);
            return false;
        }
    }

    private bool CompareByteArrays(byte[] a1, byte[] a2)
    {
        if (a1.Length != a2.Length) return false;
        for (int i = 0; i < a1.Length; i++)
        {
            if (a1[i] != a2[i]) return false;
        }
        return true;
    }

    public void StopServer()
    {
        Console.WriteLine("Stopping the server...");
        foreach (var client in clients)
        {
            client.Close();
        }
        server.Stop();
        Console.WriteLine("Server socket closed.");
    }
}

class ZoneGame
{
    private string gameGlobalPointer;
    private string clientGlobalPointer;

    public string ZGetGameGlobalPointer()
    {
        if (gameGlobalPointer == null)
        {
            Console.WriteLine("Warning: Game global pointer is not set!");
            ZSetGameGlobalPointer("DefaultPointer");
        }
        return gameGlobalPointer;
    }

    public string ZGetClientGlobalPointer()
    {
        return clientGlobalPointer;
    }

    public void ZSetGameGlobalPointer(string pointer)
    {
        gameGlobalPointer = pointer;
        Console.WriteLine("Game global pointer set to: " + gameGlobalPointer);
    }

    public void ZoneClientMessageHandler()
    {
        Console.WriteLine("Handling message for the client...");
    }

    public void ZoneClientMain()
    {
        string gamePointer = ZGetGameGlobalPointer();
        if (gamePointer != null)
        {
            Console.WriteLine("ZoneClientMain: Processing game with global pointer: " + gamePointer);
            ZoneClientMessageHandler();
        }
        else
        {
            Console.WriteLine("Failed to retrieve game global pointer.");
        }
    }
}

class Program
{
    static void Main()
    {
        ZoneGameServer server = new ZoneGameServer();
        Thread serverThread = new Thread(server.StartServer);
        serverThread.Start();

        Console.WriteLine("Press any key to stop the server...");
        Console.ReadKey();
        server.StopServer();
    }
}
