using System;
using System.Threading;
using Lidgren.Network;

namespace NetworkTesting {
    class Server {
        public static void GotMessage(object obj) {
            NetServer peer = (NetServer)obj;
            var msg = peer.ReadMessage();

            Console.WriteLine(msg.ReadString());
        }

        public static void Main(string[] args) {
            Console.WriteLine("[SERVER] Testing Lidgren-Network-v3...");
            NetPeerConfiguration serverConfig = new NetPeerConfiguration("test");
            serverConfig.EnableMessageType(NetIncomingMessageType.DiscoveryRequest);
            serverConfig.MaximumConnections = 32;
            serverConfig.Port = 12345;
            NetServer server = new NetServer(serverConfig);
            server.Start();

            SynchronizationContext.SetSynchronizationContext(new SynchronizationContext());
            server.RegisterReceivedCallback(new SendOrPostCallback(GotMessage));

            while(true) {
                string msg = Console.ReadLine();

                NetOutgoingMessage sendMsg = server.CreateMessage();
                sendMsg.Write("[SERVER] " + msg);

                server.SendToAll(sendMsg, NetDeliveryMethod.ReliableOrdered);
            }
        }
    }
}
