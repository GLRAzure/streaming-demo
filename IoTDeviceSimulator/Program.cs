using System;

using System.Threading.Tasks;

namespace IoTDeviceSimulator
{
    class Program
    {
        static void Main(string[] args)
        {
            //Get the device connection strings from the environment variable or from the first argument of the main method.
            string deviceConnections = Environment.GetEnvironmentVariable("IOTHUB_DEVICE_CONN_STRING");
            if (args.Length > 0)
            {
                deviceConnections = args[0];
            }

            //Split the connection strings by a comma.
            string[] connections = deviceConnections.Split(",");
            Console.WriteLine($"Sending messages from {connections.Length} devices.");

            int sleepInterval = 1000;
            //Build up each facade and start sending messages.
            Task[] tasks = new Task[connections.Length];
            for (int i = 0; i < connections.Length; i++) 
            {
                string connection = connections[i];

                DeviceFacade device = new DeviceFacade(connection);
                tasks[i] = Task.Run( () => device.SendMessages(sleepInterval));
                sleepInterval += 250;
            }
            Task.WaitAll(tasks);
            
        }
    }
}
