# streaming-demo

1. Provision resources using ARM template and configure (order matters):

	From the Azure portal, [deploy resources from provided template](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/quickstart-create-templates-use-the-portal#edit-and-deploy-the-template). 
	
	Template location: `deploy-template/DeployStreamingTemplate.json`.
	
	After deploying the template, you should see the following resources:
	
	![img](https://github.com/GLRAzure/streaming-demo/blob/master/img/template-resources.png)

    * Storage Account
			
      * Create a container called "demo"
      
      For help creating a container in a storage account, reference the [Microsoft documentation here](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-portal#create-a-container).
      
    * IoT Hub
			
      * Provision a minimum of two devices and Primary Connection String
      
      IMG placeholder (iot-devices)
      IMG placeholder (iot-SAS keys)
      
      Once you have the Primary Connection String for each of the two devices, concatenate both connection strings with a comma in between. This is what you will use in the IoTDeviceSimulator.
      
      * Copy Event Hub compatible endpoint
      
      IMG placeholder (iot-event-hub)
      
      * Add route(s)
      
      Add two routes:  
      
      1. To a custom Storage endpoint
      
      First, add a custom Storage endpoint and configure the following options.
      
      IMG placeholder (storage-endpoint)
      
      2. To the default events endpoint
      
      After adding both routes, you should see something similar to in your Message routing.
      
      IMG placeholder (iot-routes)
      
    * Azure SQL DB
    
      * Add client IP to firewall rules
      * Create table
      
    * Stream Analytics job
    
      * Input
      * Output
      * Query
      
    * Databricks
    
      * Notebook
			
2. Download repo and update C# with Connection String(s)
	
    * Set Environment Variable with device connection strings (concat with ",")
    * dotnet build and then dotnet run
