# streaming-demo

# Provision and configure resources using ARM template

1. From the Azure portal, [deploy resources from provided template](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/quickstart-create-templates-use-the-portal#edit-and-deploy-the-template). 
	
	Template location: `deploy-template/DeployStreamingTemplate.json`.
	
	After deploying the template, you should see the following resources:
	
	![img](https://github.com/GLRAzure/streaming-demo/blob/master/img/template-resources.png)
	
	For each of the provisioned resources, configure the following:

    * Storage Account
			
      * Create a container called "demo"
      
      For help creating a container in a storage account, reference the [Microsoft documentation here](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-portal#create-a-container).
      
    * IoT Hub
			
      * Provision a minimum of two devices and Primary Connection String
      
      ![img](https://github.com/GLRAzure/streaming-demo/blob/master/img/iot-devices.png)
      
      ![img](https://github.com/GLRAzure/streaming-demo/blob/master/img/iot-device-keys-2.png)
      
      Once you have the Primary Connection String for each of the two devices, concatenate both connection strings with a comma in between. This is what you will use in the IoTDeviceSimulator.
      
      Your concatenated connection strings will look like this:
      
      `HostName=<IOT-HUB-NAME>.azure-devices.net;DeviceId=<DEVICE-ID>;SharedAccessKey=<KEY>,HostName=<IOT-HUB-NAME>.azure-devices.net;DeviceId=<DEVICE-ID>;SharedAccessKey=<KEY>`
      
      * Copy Event Hub compatible endpoint
      
      ![img](https://github.com/GLRAzure/streaming-demo/blob/master/img/iot-event-hub.png)
      
      * Add route(s)
      
      Add two routes:  
      
      1. To a custom Storage endpoint
      
      First, add a custom Storage endpoint and configure the following options.
      
      ![img](https://github.com/GLRAzure/streaming-demo/blob/master/img/storage-endpoint.png)
      
      2. To the default events endpoint
      
      After adding both routes, you should see something similar to in your Message routing.
      
      ![img](https://github.com/GLRAzure/streaming-demo/blob/master/img/iot-routes.png)
      
    * Azure SQL DB
    
      * If necessary, add your client IP Address to the server firewall rules and open the Query Editor

      Please note that the Azure SQL Database is provisioned as serverless to help minimize costs. You may experience a brief delay when first interacting with the resource as it warms up.

      * Create table using this script:

		```
		CREATE TABLE [dbo].[sensordata](
			[city] [varchar](255) NOT NULL,
			[room] [varchar](255) NOT NULL,
			[sensor] [varchar](255) NOT NULL,
			[value] [decimal](18, 3) NOT NULL,
			[TimeReceived] [datetime2](7) NOT NULL
		)
		```
      
    * Stream Analytics job
    
      * Input
      * Output
      * Query
      
    * Databricks
    
      * Notebook
			
2. Download repo and update C# with Connection String(s)
	
    * Set Environment Variable with device connection strings (concat with ",")
    * dotnet build and then dotnet run
