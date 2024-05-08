=====================
Telemetry aggregation
=====================
Telemetry aggregation allows you to combine multiple telemetry objects into a single telemetry object by adding up all counters and errors. This allows you
for example to take ll telemetry objects created during the day and create a single daily Telemetry object that can be reported upon seperately ::

    from pipeline_telemetry import TelemetrySelector, DailyMongoAggregator

    telemetry_selection_params = TelemetrySelector(
        category=your_category,
        sub_category=your_sub_category,
        source=your_source,
        process_type=your_process_type
    )

    aggregator = DailyMongoAggregator(telemetry_selection_params)
    aggregator.aggregate_yesterday()



In this example all yesterdays telemetry object for given TelemetrySelector attributes will be aggregated into a DAILY AGGREGATION telemetry object


TelemetrySelector
-----------------
The ``TelemetrySelector`` named tuple defines which fields are needed for an aggregation selection. It is only possible to make aggregation on telemetry objects that have identical telemetry attributes category, sub_category, source and process_type. Making aggregations accross a set of telemetry objects where these attributes are not the same is not likeky to have any meaning. Fot that reason the aggregators work with ``TelemetrySelector`` objects to define the selection. 

The aggregetors themselves define the telemetry_type from which to aggregate. This implies that aggregations can only be made accross telemetry objects with identical telemetry_type, category, sub_category, source and process_type.

DailyAggregator
---------------
This aggregetor creates daily aggregations (with telemetry_type 'DAILY AGGREGATION') from selected telemetry objects with telemetry_type 'SINGLE TELEMETRY'. ``DailyAggregator`` can be instantiated as follows::

    from pipeline_telemetry import DailyAggregator, TelemetrySelector

    telemetry_selection_params = TelemetrySelector(
        category=your_category,
        sub_category=your_sub_category,
        source_name=your_source,
        process_type=your_process_type
    )

    aggregator = DailyAggregator(
        telemetry_selector=telemetry_selection_params,
        telemetry_storage=YourStorageClass())


The following methods are available for the aggregator object::

    start_date = datetime.now() - timedelta(days=10)
    start_date = datetime.now() - timedelta(days=5)
    
    # run daily aggregations for period from 10 days agon till 5 days ago.
    aggregator.aggeregate(start_date, end_date)

    # run a daily aggregation for yesterdays telemertry.
    aggregator.aggeregat_yesterda()


PartialToSingleAggregator
-------------------------
This aggregetor creates single aggregations (with telemetry_type 'SINGLE AGGREGATION') from selected telemetry objects with telemetry_type 'PARTIAL TELEMETRY'. PartialToSingleAggregators can be used when data jobs are split into sepreate jobs each creating their own partial telemetry. PartialToSingleAggregator can then be used to merge all the Partial telemetry object into a single aggregation object.


MongoDB Aggregator
------------------
A mongo DB version of the aggregator classes have been made such that you no longer have to provide the MongoDB storage class yourself.

Available MongoDB aggregators.
``DailyMongoAggregator``
``PartialToSingleyMongoAggregator``
