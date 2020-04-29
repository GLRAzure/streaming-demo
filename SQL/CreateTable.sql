SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[sensordata](
	[city] [varchar](255) NOT NULL,
	[room] [varchar](255) NOT NULL,
	[sensor] [varchar](255) NOT NULL,
	[value] [decimal](18, 3) NOT NULL,
	[TimeReceived] [datetime2](7) NOT NULL
) ON [PRIMARY]
GO