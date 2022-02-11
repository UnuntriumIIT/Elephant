using RabbitMQ.Client;
using System;
using System.Text;
using System.Threading;

namespace RabbitMqSend
{
    class Program
    {
        public static void Main()
        {
            // specify the MQ server we're connecting to
            // in our case its localhost since we're running
            // in a local docker container
            var factory = new ConnectionFactory() { HostName = "rabbitmq" };

            // 1. create connection
            using (var connection = factory.CreateConnection())

            // 2. create channel
            using (var channel = connection.CreateModel())
            {
                // 3. connect to the queue
                channel.QueueDeclare(queue: "heroes",
                                     durable: false,
                                     exclusive: false,
                                     autoDelete: false,
                                     arguments: null);

                int index = 1;
                while (index <= 99999)
                {
                    // we need to write data in the form of bytes
                    string message = $"{index}|SuperHero|Fly,Eat,Sleep,Manga|1|0|0";
                    var body = Encoding.UTF8.GetBytes(message);

                    // push content into the queue
                    channel.BasicPublish(exchange: "",
                                         routingKey: "heroes",
                                         basicProperties: null,
                                         body: body);
                    Console.WriteLine(" [x] Sent {0}", message);
                    index++;
                    Thread.Sleep(1000);
                }
            }
        }
    }
}