==========
Decorators
==========
Pipeline telemetry provides a number of decorators that help you to
automatically create and store telemetry objects when calling a method on a
class (instance).  Currently 3 decorators are available:

    - add_single_usage_telemetry
    - add_mongo_single_usage_telemetry
    - add_telemetry
    - add_mongo_telemetry



add_mongo_single_usage_telemetry
================================
Decorator method ``add_mongo_single_usage_telemetry`` adds telemetry object to
the class instance when a method with this decorator is called. The telemetry
objetc is renewed every time the decorated method is called. Hence the name
single_usage_telemetry. Telemetry objects created by this decorator are stored
in the MongoDB instance defined in by the system variables::

    from pipeline_telemetry import add_mongo_single_usage_telemetry

    class DataPipelineActivity:
        TELEMETRY_PARAMS = TELEMETRY_PARAMS_FOR_THIS_ACTIVITY

        @add_mongo_single_usage_telemetry()
        def run_data_pipeline_action(self):
            # data pipeline logic and 
            # telemetry storage actions
    
    pipeline = DataPipelineActivity()
    pipeline.run_data_pipeline_action()
    pipeline.run_data_pipeline_action()

In this example 2 telemetry objects are seperately created and stored in
MongoDB. The telemetry objects can be enriched with telemetry from with the
scope of the method. But as soon as the method is finished the telemetry object will be stored and closed.


Preset process_type counter
===========================
It is possible to add a sub_process counter to the telemetry object directly
from the single usage decorators. The sub_process must be predefined in the
ProcessType provided by ``TELEMETRY_PARAMS_FOR_THIS_ACTIVITY``::

    from pipeline_telemetry import \
        add_mongo_single_usage_telemetry, ProcessType, Telemetry


    GEO_API_PROCESS_TYPE = ProcessType(
        process_type = 'CALL_GEO_API',
        subtypes = [
            'ADDRESS_FROM_COORDINATES',
            'COORDINATES_FROM_ADDRESS']
        )

    Telemetry.add_process_type(
        process_type_key='GEO_API'
        process_type=GEO_API_PROCESS_TYPE)

    TELEMETRY_PARAMS_FOR_THIS_ACTIVITY  = {
        "category": "DATA_FROM_EXTERNAL_API",
        "sub_category": "GEO_DATA",
        "source_name": "GOOGLE",
        "process_type": ProcessTypes.GEO_API,
    }

    class DataPipelineActivity:
        TELEMETRY_PARAMS = TELEMETRY_PARAMS_FOR_THIS_ACTIVITY

        @add_mongo_single_usage_telemetry(
            sub_process='ADDRESS_FROM_COORDINATES')
        def run_data_pipeline_action(self):
            # data pipeline logic
    
    DataPipelineActivity().run_data_pipeline_action()

In this exampe a telemetry object is stored in MongoDB with a sub_process
'ADDRESS_FROM_COORDINATES' with the counter set to 1. In the decorated method itself telemetry updates are allowed but not needed to ensure that the
sub_process counter for the given sub_process is set. 
This setup is aimed a simple pipeline activities that need to only basis
counting. You will only need to decorate the method that needs to create the telemetry object in order to start recording the telemetry data.