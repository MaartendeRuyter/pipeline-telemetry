====================
Custom process types
====================
A process type is a mandatory attribute of a Telemetry object. The process type
object defines the name of the data pipeline process as well as all
subprocesses for which telemetry data needs to be recorded.
Custom process types can be defined using data class ``ProcessType`` and can
then be registered in bulk via Singleton class ``ProcessTypes`` or one by one
via class ``Telemetry``::

    from pipeline_telemetry import ProcessType, Telemetry

    GET_WEATHER_DATA = ProcessType(
        process_type = 'GET_WEATHER_DATA',
        subtypes = [
            'RETRIEVE_WEATHER_OBJECT_FROM_API',
            'CONVERT_TO_FORECAST',
            'STORE_FORECAST',
            'CONVERT_TO_CURRENT_DAY_ACTUALS',
            'STORE_ACTUALS']
    )

    Telemetry.add_process_type(
        process_type_key='GET_WEATHER_DATA',
        process_type=GET_WEATHER_DATA
    )

Once this is defined ``GET_WEATHER_DATA`` ProcessType can be used when creating
``Telemetry`` objects::

    from pipeline_telemetry import ProcessType, Telemetry

    TELEMETRY_LOAD_WEATHER_DATA = {
        'category': 'CLIMATRE',
        'sub_category': 'DAILY_WEATHER',
        'source_name': 'SOME_WEATHER_API',
        'process_type': ProcessTypes.GET_WEATHER_DATA,
        'telemetry_rules': {}
        }
    
    telemetry_obj = Telemetry(**TELEMETRY_LOAD_WEATHER_DATA)

With this telemetry object you can now add telemetry on generic level as wel as on subprocess, 'RETRIEVE_WEATHER_OBJECT_FROM_API', 'CONVERT_TO_FORECAST',
'STORE_FORECAST', 'CONVERT_TO_CURRENT_DAY_ACTUALS', 'STORE_ACTUALS'.

This foreces a unified way of telemetry reporting for this process.

ProcessTypes can be created in bulk in the following way::

    from pipeline_telemetry import \
        BaseEnumerator, ProcessType, ProcessTypes

    class WeatherDataProcessTypes(BaseEnumerator):
    """
    Class to define the process types with their subtypes for Weather data
    pipelines
    """

        GET_WEATHER_DATA = ProcessType(
            process_type = 'GET_WEATHER_DATA',
            subtypes = [
                'RETRIEVE_WEATHER_OBJECT_FROM_API',
                'CONVERT_TO_FORECAST',
                'STORE_FORECAST',
                'CONVERT_TO_CURRENT_DAY_ACTUALS',
                'STORE_ACTUALS']
        )

        GET_CLIMATE_DATA = ProcessType(
            process_type = 'GET_CLIMATE_DATA',
            subtypes = [
                'RETRIEVE_CLIMATE_OBJECT_FROM_API',
                'CONVERT_TO_YEARLY_CLIMATE_OBJECT',
                'STORE_YEARLY_CLIMATE']
        )

    ProcessTypes.register_process_types(WeatherDataProcessTypes)

Once the ``register_process_types`` class method has been called on
``ProcessTypes`` all process_types defined in the enumerator provided to the
method will be availale via ProcessTypes class for defining Telemtry objects,
like in this example::

    from pipeline_telemetry import ProcessTypes

    ProcessTypes.GET_WEATHER_DATA
    ProcessTypes.GET_CLIMATE_DATA
