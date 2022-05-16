===========================
Adding telemetry datapoints
===========================


The basics
----------
Once a telemetry object has been created in a method (or it is automatically created by using a :doc:`decorator </decorators>`) you will be able to add telemetry data to the telemetry object, for example::

    def data_pipeline():
        telemetry = Telemetry(**TELEMETRY_PARAMS)                         (1)
        data = self.get_data() # actual get data process
        telemetry.increase_sub_process_base_count('EXAMPLE_SUB_PROCESS')  (2)
        if data: 
            # if succesfull set counter for nr of data objects retrieved
            telemetry.increase_sub_process_custom_count(                  (3)
                custom_counter='DATA_POINTS',
                sub_process='EXAMPLE_SUB_PROCESS',
                increment=len(data)
                )
        else:
            # if not the fail count for the sub_process is increased
            telemetry.increase_sub_process_fail_count(                    (4)
                'EXAMPLE_SUB_PROCESS')
        
        telemetry.save_and_close()                                        (5)
        
In this example the following telemetry activities are taking place.

(1) The telemetry object is created.
(2) The base_counter for Subprocess 'EXAMPLE_SUB_PROCESS' is increased with 1.
(3) When data retrieval was succesfull, custom counter 'DATA_POINTS' within the subtype 'EXAMPLE_SUB_PROCESS' would be increased with the number of retrieved data points.
(4) When data retrieval was unsuccesfull, the fail_counter is increased.
(5) The telemetry object is saved and closed. This is needed to persist the telemetry data.

The telemetry data part of the stored telemetry object would look like this in json::

    {
        "telemetry" : {
            "EXAMPLE_SUB_PROCESS": {
                "base_counter": 1,
                "fail_counter": 0,
                "errors": null,
                "DATA_POINTS": 123
            }
        }
    } 

Or in case of an error in the data retrieval process.::

    {
        "telemetry" : {
            "EXAMPLE_SUB_PROCESS": {
                "base_counter": 1,
                "fail_counter": 1,
                "errors": null
            }
        }
    } 

There are less verbose ways of achiving the above which will be explained in the sections below.

Adding TelemetryCounters
------------------------
This package provides and easy way to define default counters that can be added to the telemetry object. Using these telemetry counters (objects of type ``TelemetryCounter``) makes your code more readable and less verbose. You can add telemetry counters directly from the ``Telemetry`` instance::

    from pipeline_telemetry import Telemetry
    from settings import counters, TELEMETRY_PARAMS

    def data_pipeline():
        telemetry = Telemetry(**TELEMETRY_PARAMS)                         
        data = self.get_data() # actual get data process
        telemetry.add_telemetry_counter(counter.GET_DATA_COUNTER)        (1)
        if data: 
            # if succesfull set counter for nr of data objects retrieved
            telemetry.add_telemetry_counter(                             (2)
                telemetry_counter=counter.ADD_DATA_POINT
                increment=len(data)
            )
        else:
            # if not the fail count for the sub_process is increased
            telemetry.add_telemetry_counter(                             (3)
                telemetry_counter=counter.FAILED_GETTING_DATA)
    
        telemetry.save_and_close()                                        

In data_pipeline() the following telemetry updates are executed:

(1) TelemetryCounter GET_DATA_COUNTER is added to the telemetry object.
(2) TelemetryCounter ADD_DATA_POINT is added to the telemetry object with an. increment equal to the length of the nr of data items returned by ``get_data()``
(3) TelemetryCounter FAILED_GETTING_DATA is added to the telemetry object when get_data doesn't return any data.
