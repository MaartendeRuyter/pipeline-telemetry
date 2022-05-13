=====
Usage
=====

This package enables a standardized way to monitor the quality and/or
performance of your datapipeline. Its main usecase is to enable easy collection
and storage of telemetry information about the collection and storage of data
in your data pipeline. 

Telemetry data is collected and stored from within a single data
collection and storage job. Each time this job is run a telemetry object will
be created accoriding to your predefined settings. Within your pipeline logic
you can then start to add telemetry data to this object. 

As each time the job runs a telemetry object will be created (and stored) you
will be able to report on the quality of your pipeline jobs by just looking at
the telemetry datapoints. For example if you were to retrieve exchange rates on
an hourly basis you could report on the number of succesfull data points
retrieved. Seeing big fluctuations in this number would be an indication of a
problem with the pipeline.::

	from pipeline_telemetry import ProcessType, Telemetry

	from settings import telemetry_params
	import counters

	class GetExchangeRatesToDollar():

		def retrieve(self, currencies_list):
			self.telemetry = Telemetry(**telemetry_params)
			# logic to retrive the currency data
			# logic to add telemetry to self.telemetry


When underlying data retrieval also report telemetry data you will be able to see any issues that might have occured throughout the data pipeline.

