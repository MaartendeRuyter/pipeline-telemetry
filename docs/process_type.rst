=============
Process types
=============
A process type is a mandatory attribute of a Telemetry object. The process type
object defines the name of the data pipeline process as well as all
subprocesses for which telemetry data can be recorded. In the example below
a process is defined for retrieving weather data. ::

    ProcessType(process_type = 'GET_WEATHER_DATA',
                subtypes = [
                    'RETRIEVE_WEATHER_OBJECT_FROM_API',
                    'CONVERT_TO_FORECAST',
                    'STORE_FORECAST']
    )

The GET_WEATHER_DATA process consists of 3 subprocesses, respectively for
retrieving, converting and storing weather forecast data. Each of these
subprocesses are allowed to have their own telemetry details.

This setup with process types foreces a unified data model for telemetry reporting in a specific datapipeline.

Available ProcessTypes
----------------------
Out of the box pipeline_telemetry defines a few process types which can be used
to store telemetry for datapipelines. 

* CREATE_DATA_FROM_URL, CREATE_DATA_FROM_API and CREATE_DATA_FROM_FILE
  
Process types that are aimed at retrieving data from web pages, api's or files. 
They all allow for the following ``subtypes``

.. list-table::
    :widths: 20 80 
    :header-rows: 1

    * - Sub process type
      - Description
    * - RETRIEVE_RAW_DATA
      - Sub process to retrieve the data from its source
    * - DATA_CONVERSION
      - Sub process to convert the data from to a form in which it can be stored
    * - DATA_STORAGE
      - Sub process to store the data that was retrieved

* UPLOAD_DATA
  
A Process type aimed at uploading (a selection of) data and uploading it to an
external environment. This process_type allows for the following ``subtypes``

.. list-table:: 
    :widths: 20 80 
    :header-rows: 1

    * - Sub process type
      - Description
    * - DATA_SELECTION
      - Sub process for selecting a set of data to be uploaded
    * - DATA_CONVERSION
      - Sub process to convert the data to a form in which it can be uploaded
    * - DATA_UPLOAD
      - Sub process to upload the data to a specific target


Creating your own process types and subtypes
--------------------------------------------
The package allows for custom process types and subtypes to be defined. This can easily be done with the ``ProcessType`` class. Be aware that your custom process types need to be registered with the ``Telemetry`` class before they can be used. In the example below the process type CUSTOM_GET_WEATHER_DATA is defined with 5 sub process types.:: 

    from pipeline_telemetry import ProcessType, Telemetry

    GET_WEATHER_DATA = ProcessType(
        process_type = 'CUSTOM_GET_WEATHER_DATA',
        subtypes = [
            'RETRIEVE_WEATHER_OBJECT_FROM_API',
            'CONVERT_TO_FORECAST',
            'STORE_FORECAST',
            'CONVERT_TO_CURRENT_DAY_ACTUALS',
            'STORE_ACTUALS']
    )


Registering process types
-------------------------

Custom process types need to be registered before they can be used in a telemetry object. This can be done the ``add_process_type`` class method on ``Telmetry`` class.::

    from pipeline_telemetry import ProcessType, Telemetry

    CUSTOM_PROCESS = ProcessType(
        process_type = 'CUSTOM_PROCESS',
        subtypes = [
            'SUB_PROCESS_1',
            'SUB_PROCESS_2']
    )

    Telemetry.add_process_type(
        process_type_key='CUSTOM_PROCESS',
        process_type=CUSTOM_PROCESS
    )

If multiple custom process types are defined you can register them in bulk using the Singleton class ``ProcessTypes``. In order to do you will need to define the process types in a child class of ``BaseEnumerator`` and call the ``register_process_types`` class method on ``ProcessTypes`` with the ``BaseEnumerator`` child class as argument.::

    from pipeline_telemetry import \
        BaseEnumerator, ProcessType, ProcessTypes

    class WeatherDataProcessTypes(BaseEnumerator):
    """
    Class to define the process types with their subtypes for Weather data
    pipelines
    """

        GET_WEATHER_DATA = ProcessType(
            process_type = 'CUSTOM_GET_WEATHER_DATA',
            subtypes = [
                'RETRIEVE_WEATHER_OBJECT_FROM_API',
                'CONVERT_TO_FORECAST',
                'STORE_FORECAST',
                'CONVERT_TO_CURRENT_DAY_ACTUALS',
                'STORE_ACTUALS']
        )

        GET_CLIMATE_DATA = ProcessType(
            process_type = 'CUSTOM_GET_CLIMATE_DATA',
            subtypes = [
                'RETRIEVE_CLIMATE_OBJECT_FROM_API',
                'CONVERT_TO_YEARLY_CLIMATE_OBJECT',
                'STORE_YEARLY_CLIMATE']
        )

    ProcessTypes.register_process_types(WeatherDataProcessTypes)

Once the ``register_process_types`` class method has been called on
``ProcessTypes`` all process_types defined in ``WeatherDataProcessTypes`` will be availale via ProcessTypes class as this examples shows.
::

    >>> from pipeline_telemetry import ProcessTypes
    >>> ProcessTypes.GET_CLIMATE_DATA
    ProcessType(process_type='CUSTOM_GET_CLIMATE_DATA', subtypes=['RETRIEVE_CLIMATE_OBJECT_FROM_API', 'CONVERT_TO_YEARLY_CLIMATE_OBJECT', 'STORE_YEARLY_CLIMATE'])


After registration ``GET_CLIMATE_DATA`` ProcessType can be used when creating
``Telemetry`` objects::

    from pipeline_telemetry import ProcessType, Telemetry

    TELEMETRY_LOAD_CLIMATE_DATA = {
        'category': 'CLIMATE',
        'sub_category': 'MONTHLY_CLIMATE_DATA',
        'source_name': 'SOME_WEATHER_API',
        'process_type': ProcessTypes.GET_CLIMATE_DATA,
        'telemetry_rules': {}
        }
    
    telemetry_obj = Telemetry(**TELEMETRY_LOAD_CLIMATE_DATA)

You can now add telemetry to this telemetry object using subprocess, 'RETRIEVE_CLIMATE_OBJECT_FROM_API', 'CONVERT_TO_YEARLY_CLIMATE_OBJECT' and 
'STORE_YEARLY_CLIMATE'.
