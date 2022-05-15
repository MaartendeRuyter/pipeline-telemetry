===============
Telemetry mixin
===============
The ``TelemetryMixin`` class is defined to allow for easy access to telemetry helper methods in a data pipeline class. The following methods are defined by the ``TelemetryMixin`` class. 


process_errors_from_return_value
--------------------------------
Method to process the errors from a ``ReturnValueWithStatus`` instance. It take a ``ReturnValueWithStatus`` object and the sub_process to which any possible errors need to be added in the telemetry object::

    from pipeline_telemetry import TelemetryMixin, add_telemetry

    form settings import TELEMETRY_PARAMS

    for my_pipeline import get_data_from_source

    
    class MyDataPipeline(TelemetryMixin):

        @add_telemetry(TELEMETRY_PARAMS)                        (1)
        def process_data(self) -> None:
            # get data in a ReturnValueWithStatus object
            return_value = get_data_from_source()               (2)
            
            # process the errors
            self.process_errors_from_return_value(              (2)
                return_value=return_value,
                sub_process="GET_DATA_FROM_SOURCE"
            )

            # if return_value is invalid it makes no sense to process
            if not return_value.is_valid:
                return

            # process the items of the retrieved data
            for record in return_value.result:
                self.process_record(record)

In process_data() is called steps are executed:

(1) ``Telemetry`` object is added to the instance of ``MyDataPipeline``
(2) The actual data is retrieved. As this method is not aware of the
    ``Telemetry`` object it can not add any errors it might encounter
(3) Errors returned by get_data_from_source are added to the telemetry object
(4) If the return_value object is not valid processing is skipped
(5) Each seperate record is processed by instance method ``process_record``. As
    this method is aware of the telemetry object you might add addational telemetry data directly form that method.



