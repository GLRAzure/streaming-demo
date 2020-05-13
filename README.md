# streaming-demo

1. Provision resources using ARM template and configure (order matters):

    * Storage Account
			
      * Create container "demo"
      
    * IoT Hub
			
      * Provision devices (min. 2)
      * Copy device keys
      * Copy Event Hub compatible endpoint
      * Add route(s)
      
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
