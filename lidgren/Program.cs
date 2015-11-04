using System;
using Lidgren.Network;

namespace XamarinTesting {
    class MainClass {
        public static void Main(string[] args) {
            Console.WriteLine("[SERVER] Testing Lidgren-Network-v3...");

            NetPeerConfiguration serverConfig = new NetPeerConfiguration("test");
            serverConfig.EnableMessageType(NetIncomingMessageType.DiscoveryRequest);
            serverConfig.MaximumConnections = 32;
            serverConfig.Port = 12345;
            NetServer server = new NetServer(serverConfig);
            server.Start();

            while(true) {
                NetIncomingMessage inc;
                while((inc = server.ReadMessage()) != null) {
                    Console.WriteLine(inc.ReadString());

//                    switch(inc.MessageType) {
//                    case NetIncomingMessageType.DiscoveryRequest:
//
//                    // Create a response and write some example data to it
//                        NetOutgoingMessage response = server.CreateMessage();
//                        response.Write("My server name");
//
//                    // Send the response to the sender of the request
//                        server.SendDiscoveryResponse(response, inc.SenderEndPoint);
//                        break;
//                    }
                }
            }
        }
    }
}
