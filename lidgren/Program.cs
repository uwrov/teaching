using System;
using System.Collections.Generic;
using System.Threading;
using Lidgren.Network;

namespace Lidgren
{
    class MainClass
    {
        public static List<NetConnection> connections = new List<NetConnection>();

        public static void GotMessage(object peer)
        {
            Console.WriteLine("sup friend");
            var msg = ((NetServer)peer).ReadMessage();
            Console.WriteLine(msg.MessageType);
            switch (msg.MessageType)
            {
                case NetIncomingMessageType.StatusChanged:
                    
                    break;

                case NetIncomingMessageType.Data:
                    // Create a response and write some example data to it
                    connections.Add(msg.SenderConnection);
                    NetOutgoingMessage response = ((NetServer)peer).CreateMessage();
                    response.Write(" Connected to: the person right next to you");
                    // Send the response to the sender of the request
                    ((NetServer)peer).SendDiscoveryResponse(response, msg.SenderEndPoint);
                    NetOutgoingMessage nextMsg = ((NetServer)peer).CreateMessage();
                    nextMsg.Write(msg.ReadString());

                    ((NetPeer)peer).SendMessage(nextMsg, connections, NetDeliveryMethod.ReliableOrdered,0);

                    break;
            }
        }

        public static void Main(string[] args)
        {
            
            Console.WriteLine("[SERVER] Testing Lidgren-Network-v3...");

            NetPeerConfiguration serverConfig = new NetPeerConfiguration("test");
            serverConfig.EnableMessageType(NetIncomingMessageType.DiscoveryRequest);
            serverConfig.EnableMessageType(NetIncomingMessageType.Data);
            serverConfig.MaximumConnections = 32;
            serverConfig.Port = 80;
            NetServer server = new NetServer(serverConfig);
            server.Start();
            SynchronizationContext.SetSynchronizationContext(new SynchronizationContext());
            var thread = new SendOrPostCallback(GotMessage);
            server.RegisterReceivedCallback(thread);
            while (true)
            {
                Console.ReadLine();
                //    NetIncomingMessage inc;
                //    while ((inc = server.ReadMessage()) != null)
                //    {


                //        switch (inc.MessageType)
                //        {
                //            case NetIncomingMessageType.DiscoveryRequest:

                //                // Create a response and write some example data to it
                //                NetOutgoingMessage response = server.CreateMessage();
                //                response.Write(" Connected to: the person right next to you");

                //                // Send the response to the sender of the request
                //                server.SendDiscoveryResponse(response, inc.SenderEndPoint);
                //                break;
                //            case NetIncomingMessageType.Data:

                //                Console.WriteLine(inc.ReadString());
                //                break;
                //        }
                //    }


            }
        }
    }
}
