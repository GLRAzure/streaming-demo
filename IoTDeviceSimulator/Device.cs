using System;
using System.Text;
using Microsoft.Azure.Devices.Client;
using System.Text.Json;
using System.Threading;

namespace IoTDeviceSimulator
{
    class DeviceFacade
    {
        private static string[] ROOMS = { "living-room", "dining-room", "family-room", "bedroom" };
        private static string[] SENSORS = { "temperature", "pressure", "humidity" };
        private static string[] CITIES = { "Pittsburgh", "Cleveland", "Rochester", "Detroit" };
        public DeviceFacade(string DeviceConnectionString)
        {
            //Strip out the device name from the connection string.
            var startIndex = DeviceConnectionString.IndexOf("DeviceId=") + 9;
            var endIndex = DeviceConnectionString.IndexOf(";",startIndex);
            this.DeviceName = DeviceConnectionString.Substring(startIndex, endIndex - startIndex);

            //Create a device connection.
            this.Device = DeviceClient.CreateFromConnectionString(DeviceConnectionString);
        }

        public DeviceClient Device { get; }
        public string DeviceName { get; }

        public void SendMessages(int sleepInterval)
        {
            while (true)
            {
                //Create a random message.    
                var rnd = new Random();
                var room = ROOMS[rnd.Next(0, ROOMS.Length)];
                var sensor = SENSORS[rnd.Next(0, SENSORS.Length)];
                var city = CITIES[rnd.Next(0, CITIES.Length)];
                double value = 0.0;
                
                // Simulate data within certain ranges based on room
                if (room == "living-room"){
                    double rand = rnd.NextDouble() * (3.0-1.0) + 1.0;
                    value = rand;
                }
                else if (room == "dining-room"){
                    double rand = rnd.NextDouble() * (5.0-3.0) + 3.0;
                    value = rand;
                }
                else if (room == "family-room"){
                    double rand = rnd.NextDouble() * (8.0-5.0) + 5.0;
                    value = rand;
                }
                else {
                    double rand = rnd.NextDouble() * (10.0-8.0) + 8.0;
                    value = rand;
                }
                    
                //Build the payload and convert it to json.
                MessagePayload payload = new MessagePayload(room, sensor, city, value);
                var message = JsonSerializer.Serialize<MessagePayload>(payload);

                //Send the message.
                Console.WriteLine($"{DeviceName}: {message}");
                Device.SendEventAsync(new Message(Encoding.UTF8.GetBytes(message))); 
                Thread.Sleep(sleepInterval);
            }
            
        }
    }

    class MessagePayload
    {
        public MessagePayload(string room, string sensor, string city, double value)
        {
            this.room = room;
            this.sensor = sensor;
            this.city = city;
            this.value = value;
        }
        public string room { get; set; }
        public string sensor { get; set; }
        public string city { get; set; }
        public double value  { get; set; }
    }
}