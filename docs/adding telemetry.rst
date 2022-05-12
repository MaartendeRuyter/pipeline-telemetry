===========================
Adding telemetry datapoints
===========================


Once a telemetry object has been created in a method (or it is automatically created by using a :doc:`decorator </decorators>`) you will be able to add telemetry data to the telemetry object, for example::

    def data_pipeline():
        telemetry = Telemetry(**TELEMETRY_PARAMS)

