====================
The Telemetry object
====================
The telemetry object which is an instance of the ``Telemetry`` class forms the
core of this package as it is used to capture relevant telemetry data during
the data retrieval and processing. The class provides many instance methods to
add telemetry data, counters and errors. Also a save method is provided to
persist the telemetry data in the database of choice (:doc:`see storage class page </storage class>`.

Initializing a telemetry object
-------------------------------
For Initializing a telemetry object the following attributes are needed

.. list-table:: Telemetry Attributes
    :widths: 16 6 6 72
    :header-rows: 1

    * - Attribute
      - Type
      - Opt/Mand
      - Description
    * - category
      - str
      - Mandatory
      - Defines data category, e.g. `Weather`
    * - sub_category
      - str
      - Mandatory
      - Free text to define data sub category, e.g. `Temperature`
    * - source_name
      - str
      - Mandatory
      - Free text to define data source, e.g. `Yahoo Weather API`
    * - process_type
      - ProcessType
      - Mandatory
      - Object that defines which data pipeline the telemetry is about
    * - telemetry_type
      - str
      - Optional
      - Value from predefined telemetry types.


These 3 identifiers allow you to find and group your telemetry data for a
specific pipeline.



Telemetry types
---------------
bla bbla

.. list-table:: Telemetry Type
    :widths: 30 70 
    :header-rows: 1

    * - Telemetry Type
      - Usage
    * - SINGLE TELEMETRY
      - Represents the full telemetry for a single data pipeline process
    * - PARTIAL TELEMETRY
      - Represents partial telemetry for a single data pipeline process
    * - DAILY AGGREGATION
      - Represents all telemetry for a single day for one or more data pipeline processes
    * - WEEKLY AGGREGATION
      - Idem for a week
    * - MONTHLY AGGREGATION
      - Idem for a month
    * - QUARTERLY AGGREGATION
      - Idem for a quarter

The SINGLE and PARTIAL TELEMETRY is usually created from a data pipeline
process itself. The AGGREGATION telemetry types will normally be created from
an aggregation process that adds up SINGLE and/or PARTIAL TELEMETRY objects.




