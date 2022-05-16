==================
Telemetry counters
==================
In order to make your code more readable you can predefine telemetry counters. These telemetry counter are instances of class TelemetryCounter and contain all required information to properly update the telemetry object according to the results in your data pipeline.::

    from counters import INVALID_DATA, PROCESSED_DATA_POINTS


    def my_data_pipeline():
        telemetry = Telemetry(**TELEMETRY_PARAMS)
        data = get_data()
        if data.invalid:
            telemetry.add_telemetry_counter(
                telemetry_counter=INVALID_DATA)
            return
        
        processed_data_points = process_data(data)
        telemetry.add_telemetry_counter(
            telemetry_counter=PROCESSED_DATA_POINTS,
            increment=len(processed_data_points))
        
        telemetry.save_and_close()

In this example two telemetry_counters define in a counters module are added to the te telemetry object. In case of successful processing of data object the number of processed data points is added to the counter defined in PROCESSED_DATA_POINTS telemetry_counter


