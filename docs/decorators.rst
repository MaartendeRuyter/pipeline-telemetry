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

add_telemetry
=============
Decorator method ``add_telemetry`` adds a telemetry object to the class
instance when a method with this decorator is called. The ``add_telemetry``
decorator checks for existing telemetry objects attached to the class instance.
If an existing telemetry object exists, no new telemetry object will be created.
This allows you to call other instance methods that also have an 
``add_telemetry`` decorator. This is helpfull when the datapipeline is
logically split into multiple sub pipelines that can also be used as stand
alone pipelines.

The telemetry object is closed after the method that created the object is finished.

Example calling a decorated method from another decoratod pipeline data method::

    from pipeline_telemetry import add_mongo_single_usage_telemetry
    from settings import TELEMETRY_PARAMS_1, TELEMETRY_PARAMS_2

    class YourDataPipelineActivity:
        
        @add_telemetry(TELEMETRY_PARAMS_1)
        def run_data_pipeline_action(self):
            # data pipeline logic and 
            # telemetry storage actions
            self.run_data_pipeline_sub_activity()
    
        @add_telemetry(TELEMETRY_PARAMS_2)
        def data_pipeline_sub_activity(self):
            # data pipeline logic and 
            # telemetry storage actions


    pipeline = DataPipelineActivity()
    pipeline.run_data_pipeline_action()

In this example a telemetry object is created based on ``TELEMETRY_PARAMS_1``
settings when ``run_data_pipeline_action`` is called. In this method pipeline
logic is executed and telemetry is added to the telemetry object. Also another
pipeline process is started called ``data_pipeline_sub_activity``. This method
has its own ``add_telemetry`` decorator where a telemetry object would be
created based on ``TELEMETRY_PARAMS_2`` settings. However because the telemetry
object created by ``run_data_pipeline_action`` still exists no new telemetry
object will be created. All telemetry storage actions done by
``data_pipeline_sub_activity`` will be stored in the telemetry object created
by ``run_data_pipeline_action``.
This telemetry object will be closed once ``run_data_pipeline_action`` is
finished. This is done automatically by the ``add_telemetry``.

Example directly calling the ``data_pipeline_sub_activity``::

    pipeline.data_pipeline_sub_activity()

When you directly call the ``data_pipeline_sub_activity`` a telemetry object will be created based upon ``TELEMETRY_PARAMS_2`` settings and all telemetry data created in that method will go to that telemetry object.
    

add_mongo_telemetry
===================
This decorator works exactly the same as the ``add_telemetry`` decorator. The
telemetry objects are however stored in a MongoDB instance


add_single_usage_telemetry
==========================
Decorator method ``add_single_usage_telemetry`` also adds a telemetry object to
the class instance when a method with this decorator is called. The telemetry
object is however renewed every time the decorated method is called (or
overwritten when another decorator is called). Hence the name
single_usage_telemetry. 

When using this decorator you should not call other methods with telemetry
decorators. Its use is aimed at methods that handle all the telemetry updates
within the scope of a single data pipeline method.

Example::

    from pipeline_telemetry import add_mongo_single_usage_telemetry

    class DataPipelineActivity:
        TELEMETRY_PARAMS = TELEMETRY_PARAMS_FOR_THIS_CLASS§

        @add_single_usage_telemetry()
        def run_data_pipeline_action(self):
            # data pipeline logic and 
            # telemetry storage actions
    
    pipeline = DataPipelineActivity()
    pipeline.run_data_pipeline_action()
    pipeline.run_data_pipeline_action()

In this example 2 telemetry objects are seperately created and stored in
MongoDB. The telemetry objects can be enriched with telemetry from with the
scope of the method. As soon as the method is finished the telemetry object will be stored and closed.

telemetry parameters for add_single_usage_telemetry
===================================================
When using the ``add_single_usage_telemetry`` decorator you will have to define
the telemetry details at class level. This can be done in the following way::

        class DataPipelineActivity:
            TELEMETRY_PARAMS = TELEMETRY_PARAMS_FOR_THIS_CLASS

Where class attribute ``TELEMETRY_PARAMS`` is assigned to a valid set of
telemetry parameters. All methods decorated with ``add_single_usage_telemetry``
type decorators will use class attribute ``TELEMETRY_PARAMS`` as the source for
telemetry parameters.

add_mongo_single_usage_telemetry
================================
This decorator works exactly the same as the ``add_single_usage_telemetry``
decorator. The telemetry objects are however stored in a MongoDB instance

Preset process_type counter
===========================
It is possible to add a sub_process counter to the telemetry object directly
from the single usage decorators. The sub_process must be predefined in the
ProcessType provided by ``TELEMETRY_PARAMS_FOR_THIS_ACTIVITY``::

    from pipeline_telemetry import \
        add_mongo_single_usage_telemetry, ProcessType, Telemetry
    from settings import TELEMETRY_PARAMS_FOR_THIS_CLASS

    class DataPipelineActivity:
        TELEMETRY_PARAMS = TELEMETRY_PARAMS_FOR_THIS_CLASS

        @add_mongo_single_usage_telemetry(
            sub_process='ADDRESS_FROM_COORDINATES')
        def run_data_pipeline_action(self):
            # data pipeline logic
            # telemetry storage actions
    
    DataPipelineActivity().run_data_pipeline_action()

In this exampe a telemetry object is stored in MongoDB with a sub_process
'ADDRESS_FROM_COORDINATES' with the counter set to 1. In the decorated method
itself telemetry updates are allowed but no longer needed to ensure that the
sub_process counter for the given sub_process is set. 
This setup is aimed a simple pipeline activities that need to only basis
counting. You will only need to decorate the method that needs to create the telemetry object in order to start recording the telemetry data.