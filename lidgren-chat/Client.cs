using System;
using System.Threading;
using Lidgren.Network;

namespace NetworkTesting {
    public class Client {
        public static void GotMessage(object obj) {
            NetClient peer = (NetClient)obj;
            var msg = peer.ReadMessage();

            Console.WriteLine(msg.ReadString());
        }

        static public void Main(string[] args) {
            Console.WriteLine("[CLIENT] Testing Lidgren-Network-v3...");

            NetPeerConfiguration clientConfig = new NetPeerConfiguration("test");
            clientConfig.EnableMessageType(NetIncomingMessageType.DiscoveryResponse);
            NetClient client = new NetClient(clientConfig);
            client.Start();

            SynchronizationContext.SetSynchronizationContext(new SynchronizationContext());
            client.RegisterReceivedCallback(new SendOrPostCallback(GotMessage));

            Console.WriteLine("IP to connect to: ");
            String ip = Console.ReadLine();

            client.Connect(new System.Net.IPEndPoint(System.Net.IPAddress.Parse(ip), 12345));

            while(true) {
                string msg = Console.ReadLine();

                NetOutgoingMessage sendMsg = client.CreateMessage();
                sendMsg.Write("[CLIENT] " + msg);
                client.SendMessage(sendMsg, NetDeliveryMethod.ReliableOrdered);
            }
        }
    }
}

