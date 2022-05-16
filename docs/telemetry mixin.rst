===============
Telemetry mixin
===============
The ``TelemetryMixin`` class is defined to allow for easy access to telemetry helper methods in a data pipeline class. The following methods are defined by the ``TelemetryMixin`` class. 


process_errors_from_return_value
--------------------------------
Method to process the errors from a ``ReturnValueWithStatus`` instance. It takes a ``ReturnValueWithStatus`` object and the sub_process to which any possible errors need to be added in the telemetry object::

    from pipeline_telemetry import TelemetryMixin, add_telemetry

    form settings import TELEMETRY_PARAMS

    for my_pipeline import get_data_from_source

    
    class MyDataPipeline(TelemetryMixin):

        @add_telemetry(TELEMETRY_PARAMS)                        (1)
        def process_data(self) -> None:
            # get data in a ReturnValueWithStatus object
            return_value = get_data_from_source()               (2)
            
            # process the errors
            self.process_errors_from_return_value(              (3)
                return_value=return_value,
                sub_process="GET_DATA_FROM_SOURCE"
            )

            # if return_value is invalid it makes no sense to process
            if not return_value.is_valid:                       (4)
                return

            # process the items of the retrieved data
            for record in return_value.result:                  (5)
                self.process_record(record)

When process_data() is called the following steps are executed:

(1) ``Telemetry`` object is added to the instance of ``MyDataPipeline``
(2) The actual data is retrieved. As this method is not aware of the
    ``Telemetry`` object it can not add any errors it might encounter
(3) Errors returned by get_data_from_source are added to the telemetry object
(4) If the return_value object is not valid processing is skipped
(5) Each seperate record is processed by instance method ``process_record``. As
    this method is aware of the telemetry object you might add addational telemetry data directly form that method.


process_telemetry_counters_from_return_value
--------------------------------------------
Method to process the telemetry counters from a ``ReturnValueWithStatus`` instance. It takes a ``ReturnValueWithStatus`` object and processes all the telemetry counters that are found in the return_value's result attribute. The method returns the result attribute without the telemetry counters.::

    from pipeline_telemetry import TelemetryMixin, add_telemetry

    form settings import TELEMETRY_PARAMS

    for my_pipeline import get_data_from_source

    
    class MyDataPipeline(TelemetryMixin):

        @add_telemetry(TELEMETRY_PARAMS)                        
        def process_data(self) -> None:
            # get data in a ReturnValueWithStatus object
            return_value = get_data_from_source()               
            
            # process the telemetry_counters
            result_without_telemetry_counters = \               (1)
                self.process_telemetry_counters_from_return_value(              
                    return_value=return_value)

            # process the items of the retrieved data
            for record in result_without_telemetry_counters:    (2)
                self.process_record(record)

When process_data() is called the following steps are executed:

(1) All telemetry counters returned in the return_value.result by ``get_data_from_source()`` method are added to the telemetry attribute of the ``MyDataPipeline`` instance.
(2) Any remaining data items can now be process by ``process_record`` method.



