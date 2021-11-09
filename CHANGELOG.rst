
Changelog
=========

0.0.1 (2021-10-06)
------------------

* First release on PyPI.


0.0.4 (2021-10-31)
------------------

* Seperated the storage module
* Added MongoDb storage class
* Started with documentation

0.1.0 (2021-11-05)
------------------

* added Telemetry method add_telemetry_counter 
* Added ``TelemetryCounter`` class that can be used to make prefedined objects
  that can be added to the Telemetry instance with the add_telemetry_counter
  method. This will improve readibilty of your code::

    from pipeline_telemetry import TelemetryCounter

    YOUR_PREDFINED_COUNTER = (
        process_type=ProcessTypes.CREATE_DATA_FROM_API,
        sub_process='RETRIEVE_RAW_DATA',
        counter_name='my_custom_counter',
    )

    telemetry.add_telemetry_counter(YOUR_PREDFINED_COUNTER)


0.2.0 (2021-11-09)
------------------

* added error field to ``TelemetryCounter`` so that default Errorcodes
  can be used in a ``TelemetryCounter`` instance to keep an error counter
  in the telemetry
* Updated add_telemetry_counter so that it can handle TelemetryCounter instances
  with either an Errorcode of a custom counter. In case of ErrorCode the actual
  error_code will serve as the customer counter. 


0.2.1 (2021-11-09)
------------------

* added ``is_telemetry_counter`` method in helper module
* moved ``add_telemetry`` decorator to helper module
* both method can be directly imported from ``pipeline_telemetry`` module