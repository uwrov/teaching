using System;
using Lidgren.Network;

namespace XamarinTesting {
    public class Client {
        static public void Main(string[] args) {
            Console.WriteLine("[CLIENT] Testing Lidgren-Network-v3...");

            NetPeerConfiguration clientConfig = new NetPeerConfiguration("test");
            clientConfig.EnableMessageType(NetIncomingMessageType.DiscoveryResponse);
            NetClient client = new NetClient(clientConfig);
            client.Start();

            Console.WriteLine("IP to connect to: ");
            String ip = Console.ReadLine();
            client.Connect(ip, 12345);

            while(true) {
                if(client.ServerConnection != null) {
                    string msg = Console.ReadLine();

                    NetOutgoingMessage sendMsg = client.CreateMessage();
                    sendMsg.Write(msg);
                    client.SendMessage(sendMsg, NetDeliveryMethod.ReliableOrdered);
                }
            }
        }
    }
}

