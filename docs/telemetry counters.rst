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

In this example two telemetry_counters define in a counters module are added to the telemetry object. In case of successful processing of data object the number of processed data points is added to the counter defined in PROCESSED_DATA_POINTS telemetry_counter

set_increment
-------------

When a telemetry counter is added to a result in a different class from where the telementry object is stored you will not be able to overide the increment when adding the counter to the telemetry object (See previous example). As ``TelementryCounter`` object is non mutable is not possible to update the increment in the predefined counter object. The ``set_increment`` method was created to bypass this. Calling the method with the new increment as argument on an existing counter will return a copy of that counter with an updated increment.::

    >>> form settings import PREDEFINED_COUNTER
    >>> PREDEFINED_COUNTER.increment
    1
    >>> new_counter = PREDEFINED_COUNTER.set_increment(increment=10)
    >>> new_counter.increment
    10

Now you can freely change the increment of the predefined counter and return it to the class that adds the counter to the telemetry object.

hash
----
In order to easily count the number of ``TelemetryCounters`` in a list a hash method has been implemented on the TelemetryCounters. TelemetryCounters with differerent cvalue
