# streaming-demo

This repository contains assets for quickly building out an end-to-end streaming demo that can serve as a foundation for a PoC or MVP. Included in this repository is an ARM template for deploying the key resources in Azure and a data generator that simulates device telemetry data. Below is more detailed documentation for configuring resources after they have been deployed in Azure.

# Provision and configure resources using ARM template

From the Azure portal, [deploy resources from provided template](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/quickstart-create-templates-use-the-portal#edit-and-deploy-the-template). 
	
Template location: `deploy-template/DeployStreamingTemplate.json`.

After deploying the template, you should see the following resources:

![img](https://github.com/GLRAzure/streaming-demo/blob/master/img/template-resources-01.png)

For each of the provisioned resources, configure the following:

## Storage Account

* Create a container called "demo"
      
For help creating a container in a storage account, reference the [Microsoft documentation here](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-portal#create-a-container).
      
## IoT Hub
			
* Provision a minimum of two devices and Primary Connection String
      
![img](https://github.com/GLRAzure/streaming-demo/blob/master/img/iot-devices.png)

![img](https://github.com/GLRAzure/streaming-demo/blob/master/img/iot-device-keys-2.png)
      
Once you have the Primary Connection String for each of the two devices, concatenate both connection strings with a comma in between. This is what you will use in the IoTDeviceSimulator.

Your concatenated connection strings will look like this:

`HostName=<IOT-HUB-NAME>.azure-devices.net;DeviceId=<DEVICE-ID>;SharedAccessKey=<KEY>,HostName=<IOT-HUB-NAME>.azure-devices.net;DeviceId=<DEVICE-ID>;SharedAccessKey=<KEY>`
      
* Copy Event Hub compatible endpoint
      
![img](https://github.com/GLRAzure/streaming-demo/blob/master/img/iot-event-hub.png)

Add this Event Hub compatible endpoint to your Key Vault with the secret name `eventhubsreader`.

After adding this Secret, your Key Vault will look similar to this:

![img](https://github.com/GLRAzure/streaming-demo/blob/master/img/kv-secret.png)
      
* Add route(s)

Add two routes:  

1. To a custom Storage endpoint

First, add a custom Storage endpoint and configure the following options.

![img](https://github.com/GLRAzure/streaming-demo/blob/master/img/storage-endpoint.png)

2. To the default events endpoint

After adding both routes, you should see something similar to in your Message routing.

![img](https://github.com/GLRAzure/streaming-demo/blob/master/img/iot-routes.png)
      
## Azure SQL DB
    
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
      
## Stream Analytics job
    
* Input

Add an input that points to the device telemetry from IoT Hub.

![img](https://github.com/GLRAzure/streaming-demo/blob/master/img/sa-input.png)

* Output

Add two outputs: one that points to a Power BI streaming dataset and another that points to an Azure SQL DB.

![img](https://github.com/GLRAzure/streaming-demo/blob/master/img/sa-powerbi-output.png)

![img](https://github.com/GLRAzure/streaming-demo/blob/master/img/sa-sql-output.png)

* Query

Add the following query to link the input with the two outputs:

Query location: `Stream Analytics/sademo/Transformation.asaql`
      
## Databricks

* Create a Key Vault-backed secret scope

Follow the instructions located here to [add a secret scope backed by Azure Key Vault](https://docs.microsoft.com/en-us/azure/databricks/security/secrets/secret-scopes#--create-an-azure-key-vault-backed-secret-scope).

* Create cluster and add a Maven coordinate

Create a new cluster with similar configurations:

![img](https://github.com/GLRAzure/streaming-demo/blob/master/img/adb-cluster.png)

Add this Maven coordinate for compatibility with IoT Hub: `com.microsoft.azure:azure-eventhubs-spark_2.11:2.3.6`

![img](https://github.com/GLRAzure/streaming-demo/blob/master/img/adb-maven.png)

* Import Notebook and run all cells

Import the DBC archive notebook located at this location: `notebooks/Streaming Demo.dbc`

After running the cells, select `View: Streaming Dashboard`.
			
## Run the IoTDeviceSimulator
	
* Set Environment Variable with device connection strings (concat with ",")

Create a new system Environment Variable called: `IOTHUB_DEVICE_CONN_STRING`

For it's value, add the concatenated connection strings for each of the devices you created earlier. It should look like this:

`HostName=<IOT-HUB-NAME>.azure-devices.net;DeviceId=<DEVICE-ID>;SharedAccessKey=<KEY>,HostName=<IOT-HUB-NAME>.azure-devices.net;DeviceId=<DEVICE-ID>;SharedAccessKey=<KEY>`

* Run the Device simulator

Use `dotnet build` and then `dotnet run` from the `IoTDeviceSimulator` directory.

You should see output similar to this after running the device simulator:

![img](https://github.com/GLRAzure/streaming-demo/blob/master/img/device-output.png)
