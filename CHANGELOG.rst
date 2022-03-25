
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
* both methods can be directly imported from ``pipeline_telemetry`` module

0.2.2 (2021-11-10)
------------------

* added ``add_mongo_telemetry`` decorator that uses mongo storage class

0.2.3 (2021-11-10)
------------------

* Added attribute ``process_types`` to ``TelemetryCounter`` dataclass next to
  existing ``process_type`` attribute. This allows you to choose between a list
  of process_types or just a single process_type to be in scope of the ``TelemetryCounter``` instance
  

0.2.4 (2021-11-11)
------------------

* Implemented ``add_to`` method in ``TelemetryCounter``. Can be used to  add a
  ``TelemetryCounter`` instance to an object with a telemetry instance attached
  to it. This will make the code more readable.

0.2.5 (2021-11-11)
------------------

* Implemented ``increase_base_count`` and ``increase_fail_count`` method. They
  can be used to make your code more readable when updating the telemetry


0.2.6 (2021-12-08)
------------------

* Added default increment value = 1 to methods ``increase_base_count`` and
  ``increase_fail_count``

0.2.7 (2022-01-13)
------------------

* Added fields ``category`` and ``sub_category`` to the telemetry object to
  allow for better distinction between telemetry sources
* Rename telemetry field 'process_name' to 'soure_name' to be more clear about
  the data source in scope of the telemetry object

0.2.8 (2022-01-13)
------------------

* Fix in storage classes to ensure ``category`` and ``sub_category`` to be
  stored in the toplevel of the telemetry object

0.2.10 (2022-01-18)
-------------------

* Added indexes to mongo storage class

0.2.11 (2022-01-18)
-------------------

* Added ``created_at`` field in mongo storage class for better date selection
* of the telemetry objects

0.2.12 (2022-01-19)
-------------------

* Added ``traffic_light`` attribute to Telemetry object indicating the success
  state of the datapipeline process that is reporting on
* Some minor refactoring

0.2.16 (2022-02-01)
-------------------

* Added ``telemetry_type`` and ``io_time_in_seconds`` attributes to Telemetry
* object including a method to increase ``io_time_in_seconds``.


0.2.18 (2022-03-2)
-------------------

* Added ``add_single_usage_telemetry`` decorator to be used for single usage
* telemetry objects
