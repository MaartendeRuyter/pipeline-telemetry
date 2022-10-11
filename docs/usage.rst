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


When underlying data retrieval also report telemetry data you will be able to see any issues that might have occured throughout the data pipeline. An example telemetry object could look like::

	{
		"telemetry_type": "SINGLE TELEMETRY",
		"category": "CURRENCIES",
		"sub_category": "DAILY_EXCHANGE_RATES",
		"source_name": "FOREX_MARKETS_API",
		"process_type": "RETRIEVE_DAILY_EXCHANGE_RATES",
		"start_date_time": 2022-01-19 17:38:04.696Z,
		"run_time_in_seconds": 19.4553,
		"io_time_in_seconds": 9.5542,
		"traffic_light": "GREEN",
		"telemetry": {
			"GET_DATA_FROM_API" : {
				"base_counter": 85,
				"fail_counter": 2,
				"counters": {
					"RETRIEV_DATA_FROM_API": 84,
					"FORMAT_DATE_FIELD": 83},
				"errors": {
					"RESPONSE_STATUS_CODE_404": 1,
					"CONV_DATE_001": 1}
				},
			"STORE_EXCHANGE_RATE" : {
				"base_counter": 83,
				"fail_counter": 2,
				"counters": {
					"STORE_EXCHANGE_RATE_SUCCESS": 81},
				"errors": {
					"UNKNOWN_EXCHANGE_RATE": 2}
			},
		}
	}

In this example a daily pipeline for retrieving exchange rates has created a telemetry object. The pipeline tried to call the exchange rate api 85 times. 84 times it got a succesfull response and 1 time it got a 404 response. For 1 response the pipline was not able to convert the datefield properly. 
This resulted in 83 attempts to store an exchange rate, for 2 cases this failed because the exchange rate was unknown. 
The pipeline_telemetry package provides you with easy to use methods and decorators to create the telemetry objects and add customer counters and errors to the telemetry.
 





